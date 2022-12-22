from __future__ import annotations

import typing

from pydbm import typing_extra
from pydbm.database import DatabaseManager
from pydbm.exceptions import PydbmBaseException
from pydbm.inspect_extra import get_obj_annotations
from pydbm.models.fields import AutoField, Field, Undefined

__all__ = (
    "Meta",
)


PRIMARY_KEY: typing.Final[str] = "pk"  # unexport: not-public
UNIQUE_TOGETHER = ()  # unexport: not-public
CLASS_CONFIG_NAME: typing.Final[str] = "Config"  # unexport: not-public


class Config(typing.NamedTuple):  # unexport: not-public
    table_name: str
    unique_together: tuple[str, ...]


@typing_extra.dataclass_transform(kw_only_default=True, field_specifiers=(Field,))
class Meta(type):
    if typing.TYPE_CHECKING:
        not_required_fields: list[Field | AutoField]
        required_fields: list[str]
        database: DatabaseManager

    @staticmethod
    def __new__(mcs, cls_name: str, bases: tuple[Meta, ...], namespace: dict[str, typing.Any], **kwargs: typing.Any) -> type:  # noqa: E501
        if not [b for b in bases if isinstance(b, mcs)]:
            namespace["__slots__"] = mcs.generate_slots(namespace) + ("fields", "id")
            return super().__new__(mcs, cls_name, bases, namespace)

        namespace["__slots__"] = mcs.generate_slots(namespace) + ("database",)
        return super().__new__(mcs, cls_name, bases, namespace)

    def __init__(cls, cls_name: str, bases: tuple[Meta, ...], namespace: dict[str, typing.Any], **kwargs: typing.Any) -> None:  # noqa: E501
        super().__init__(cls_name, bases, namespace, **kwargs)
        if [b for b in bases if isinstance(b, type(cls))]:
            mcs = type(cls)

            config = mcs.get_config(cls_name, namespace)
            fields = mcs.generate_fields(cls, cls_name, namespace)

            cls.required_fields, cls.not_required_fields = mcs.split_fields(list(fields.values()))
            cls.objects = DatabaseManager(model=cls, table_name=config.table_name)  # type: ignore
            cls.DoesNotExists = type("DoesNotExists", (PydbmBaseException,), {"__doc__": "Exception for not found id in the models."})  # noqa: E501

            for key, value in fields.items():
                setattr(cls, key, value)

    def __call__(cls, **kwargs):
        for field in cls.not_required_fields:
            if field.public_name not in kwargs and field.public_name != PRIMARY_KEY:
                kwargs[field.public_name] = field.get_default_value()  # type: ignore[attr-defined]  # noqa: E501

        for field in cls.required_fields:  # type: ignore[assignment]
            if field not in kwargs:
                raise ValueError(f"{field} is required")

        primary_key_field: AutoField | None = next(  # TODO: Always AutoField must be exists ?
            filter(
                lambda field: field.public_name not in kwargs and field.public_name == PRIMARY_KEY,  # type: ignore[arg-type]  # noqa: E501
                cls.not_required_fields,
            ),
            None,
        )
        if primary_key_field:
            kwargs[primary_key_field.public_name] = primary_key_field(kwargs).get_default_value()  # type: ignore[attr-defined]  # noqa: E501

        return super().__call__(**kwargs)

    @classmethod
    def get_config(mcs, cls_name: str, namespace: dict[str, typing.Any]) -> Config:
        config: Config | None = namespace.get(CLASS_CONFIG_NAME, None)

        if config is not None:
            table_name = config.table_name if hasattr(config, "table_name") else mcs.generate_table_name(cls_name)
            unique_together = config.unique_together if hasattr(config, "unique_together") else UNIQUE_TOGETHER
        else:
            table_name = mcs.generate_table_name(cls_name)
            unique_together = UNIQUE_TOGETHER

        return Config(table_name, unique_together)

    @staticmethod
    def generate_table_name(cls_name: str) -> str:
        return f"{cls_name.lower()}s"

    @classmethod
    def generate_slots(mcs, namespace: dict[str, typing.Any]) -> tuple[str, ...]:
        slots = {"_pk"}
        ann = namespace.get("__annotations__", {})
        for field_name, field_type in ann.items():
            private_name = "_" + field_name
            slots.add(private_name)
        return tuple(sorted(slots))

    @classmethod
    def generate_fields(mcs, cls, cls_name: str, namespace: dict[str, typing.Any]) -> dict[str, Field | AutoField]:
        """Inspect namespace and return fields."""
        fields: dict[str, Field | AutoField] = {}
        ann = get_obj_annotations(obj=cls)

        for field_name, field_type in ann.items():
            default_value: Field | typing.Any = namespace.get(field_name, Undefined)
            field = default_value if isinstance(default_value, Field) else Field(default=default_value)
            fields.update({field_name: field(field_name, field_type)})

        unique_together = mcs.get_config(cls_name, namespace).unique_together or tuple(fields.keys())
        fields[PRIMARY_KEY] = AutoField("pk", str, unique_together=unique_together)
        return fields

    @staticmethod
    def split_fields(fields: list[Field | AutoField]) -> tuple[list[str], list[Field | AutoField]]:
        required_fields: list[str] = []
        not_required_fields: list[Field | AutoField] = []

        for field in fields:
            if field.is_required():
                required_fields.append(field.public_name)
            else:
                not_required_fields.append(field)
        return required_fields, not_required_fields
