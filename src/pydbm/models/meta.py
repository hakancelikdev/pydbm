from __future__ import annotations

import typing

from pydbm import typing_extra
from pydbm.database import Database
from pydbm.models.fields import AutoField, Field, Undefined

__all__ = ["CLASS_CONFIG_NAME", "Config", "Meta", "PRIMARY_KEY", "UNIQUE_TOGETHER"]


PRIMARY_KEY: typing.Final[str] = "pk"
UNIQUE_TOGETHER = ()
CLASS_CONFIG_NAME: typing.Final[str] = "Config"


class Config(typing.NamedTuple):
    table_name: str
    unique_together: tuple[str, ...]


@typing_extra.dataclass_transform(kw_only_default=True, field_specifiers=(Field,))
class Meta(type):
    if typing.TYPE_CHECKING:
        not_required_fields: list[Field | AutoField]
        required_fields: list[str]
        database: Database

    def __new__(
        mcs,
        cls_name: str,
        bases: tuple[Meta, ...],
        namespace: dict[str, typing.Any],
        **kwargs: typing.Any,
    ) -> type:
        if not [b for b in bases if isinstance(b, mcs)]:
            return super().__new__(mcs, cls_name, bases, namespace, **kwargs)

        namespace["__slots__"] = mcs.generate_slots(cls_name, namespace)
        return super().__new__(mcs, cls_name, bases, namespace, **kwargs)

    def __init__(
        cls, cls_name: str, bases: tuple[Meta, ...], namespace: dict[str, typing.Any], **kwargs: typing.Any
    ) -> None:
        super().__init__(cls_name, bases, namespace, **kwargs)

        mcs = Meta

        config = mcs.get_config(cls_name, namespace)
        fields = mcs.generate_fields(cls_name, namespace)

        cls.required_fields, cls.not_required_fields = mcs.split_fields(list(fields.values()))
        cls.database = Database(table_name=config.table_name)

        for key, value in fields.items():
            setattr(cls, key, value)

    def __call__(cls, **kwargs):
        for field in cls.not_required_fields:
            if field.public_name not in kwargs and field.public_name != PRIMARY_KEY:
                kwargs[field.public_name] = field.get_default_value()  # type: ignore[attr-defined]  # noqa: E501

        for field in cls.required_fields:  # type: ignore[assignment]
            if field not in kwargs:
                raise ValueError(f"{field} is required")

        primary_key_field: AutoField | None = next(
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
    def generate_slots(mcs, cls_name, namespace: dict[str, typing.Any]) -> tuple[str, ...]:
        fields = mcs.generate_fields(cls_name, namespace)
        return tuple(sorted({field.private_name for field in fields.values()}))

    @classmethod
    def generate_fields(mcs, cls_name: str, namespace: dict[str, typing.Any]) -> dict[str, Field | AutoField]:
        """Inspect namespace and return fields."""
        config = mcs.get_config(cls_name, namespace)

        fields: dict[str, Field | AutoField] = {}
        ann = namespace.get("__annotations__", {})

        for field_name, field_type_or_type_name in ann.items():
            if not isinstance(field_type_or_type_name, str):
                field_type_name = field_type_or_type_name.__name__
            else:
                field_type_name = field_type_or_type_name

            default: Field | typing.Any = namespace.get(field_name, Undefined)
            field = default if isinstance(default, Field) else Field(default=default)
            fields.update(**{field_name: field(field_name, field_type_name)})

        unique_together: tuple[str, ...] = config.unique_together or tuple(fields.keys())
        fields[PRIMARY_KEY] = AutoField("pk", "str", unique_together=unique_together)

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
