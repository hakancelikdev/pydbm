from __future__ import annotations

import typing

from pydbm import contstant as C
from pydbm import typing_extra
from pydbm.database import DatabaseManager
from pydbm.exceptions import EmptyModelError, PydbmBaseException, UnnecessaryParamsError
from pydbm.inspect_extra import get_obj_annotations
from pydbm.models.fields import AutoField, Field, Undefined

__all__ = (
    "Meta",
)


class Config(typing.NamedTuple):  # unexport: not-public
    table_name: str
    unique_together: tuple[str, ...]


@typing_extra.dataclass_transform(kw_only_default=True, field_specifiers=(Field,))
class Meta(type):
    if typing.TYPE_CHECKING:
        not_required_fields: list[Field | AutoField]
        required_fields: list[str]
        objects: DatabaseManager
        DoesNotExists: typing.Type[PydbmBaseException]
        fields: dict[str, typing.Any]

    @staticmethod
    def __new__(mcs, cls_name: str, bases: tuple[Meta, ...], namespace: dict[str, typing.Any], **kwargs: typing.Any) -> type:  # noqa: E501
        annotations = namespace.pop("__annotations__", {})
        annotations[C.PRIMARY_KEY] = str
        slots = mcs.generate_slots(annotations)
        if not [b for b in bases if isinstance(b, mcs)]:
            slots.remove("_id")
            slots.append("fields")
        else:
            if not annotations or list(annotations.keys()) == [C.PRIMARY_KEY]:
                raise EmptyModelError("Empty model is not allowed.")
            slots.append("database")

        namespace["__slots__"] = tuple(slots)
        namespace["__annotations__"] = annotations
        return super().__new__(mcs, cls_name, bases, namespace)

    def __init__(cls, cls_name: str, bases: tuple[Meta, ...], namespace: dict[str, typing.Any], **kwargs: typing.Any) -> None:  # noqa: E501
        super().__init__(cls_name, bases, namespace, **kwargs)
        if [b for b in bases if isinstance(b, type(cls))]:
            mcs = type(cls)

            cls._config = mcs.get_config(cls, cls_name, namespace)
            fields = mcs.generate_fields(cls, cls_name, namespace)

            cls.required_fields, cls.not_required_fields = mcs.split_fields(list(fields.values()))
            cls.objects = DatabaseManager(model=cls, table_name=cls._config.table_name)  # type: ignore
            cls.DoesNotExists = type("DoesNotExists", (PydbmBaseException,), {"__doc__": "Exception for not found id in the models."})  # type: ignore # noqa: E501
            cls.RiskofReturningMultipleObjects = type("RiskofReturningMultipleObjects", (PydbmBaseException,), {"__doc__": "Exception for risk of returning multiple objects."})  # noqa: E501

            for key, value in fields.items():
                setattr(cls, key, value)

    def __call__(cls, **kwargs):
        for extra_field_name in (set(kwargs.keys()) - set(cls.__annotations__.keys())):
            raise UnnecessaryParamsError(f"{extra_field_name} is not defined in {cls.__name__}")

        for field in cls.not_required_fields:
            if field.public_name not in kwargs and field.public_name != C.PRIMARY_KEY:
                kwargs[field.public_name] = field.get_default_value()  # type: ignore[attr-defined]  # noqa: E501

        for field in cls.required_fields:  # type: ignore[assignment]
            if field not in kwargs:
                raise ValueError(f"{field} is required")

        for not_required_field in cls.not_required_fields:
            if not_required_field.public_name not in kwargs and not_required_field.public_name == C.PRIMARY_KEY:
                kwargs[not_required_field.public_name] = not_required_field(kwargs).get_default_value()  # type: ignore[call-arg, arg-type]  # noqa: E501
                break

        return super().__call__(**kwargs)

    @classmethod
    def get_config(mcs, cls, cls_name: str, namespace: dict[str, typing.Any]) -> Config:
        config: Config | None = namespace.get(C.CLASS_CONFIG_NAME, None)

        if config is not None:
            table_name = config.table_name if hasattr(config, "table_name") else mcs.generate_table_name(cls_name)
            unique_together = config.unique_together if hasattr(config, "unique_together") else C.UNIQUE_TOGETHER
        else:
            table_name = mcs.generate_table_name(cls_name)
            unique_together = C.UNIQUE_TOGETHER

        if not unique_together:
            ann = get_obj_annotations(obj=cls)
            ann.pop(C.PRIMARY_KEY, None)  # NOTE: Remove primary key from unique_together
            unique_together = tuple(ann.keys())

        return Config(table_name, unique_together)

    @staticmethod
    def generate_table_name(cls_name: str) -> str:
        return f"{cls_name.lower()}s"

    @classmethod
    def generate_slots(mcs, annotations: dict[str, typing.Any]) -> list[str]:
        slots = set()
        for field_name, field_type in annotations.items():
            private_name = "_" + field_name
            slots.add(private_name)
        return sorted(slots)

    @classmethod
    def generate_fields(mcs, cls, cls_name: str, namespace: dict[str, typing.Any]) -> dict[str, Field | AutoField]:
        """Inspect namespace and return fields."""
        fields: dict[str, Field | AutoField] = {
            C.PRIMARY_KEY: AutoField(C.PRIMARY_KEY, str, unique_together=cls._config.unique_together)
        }
        for field_name, field_type in get_obj_annotations(obj=cls).items():
            if field_name == C.PRIMARY_KEY:
                continue

            default_value: Field | typing.Any = namespace.get(field_name, Undefined)
            field = default_value if isinstance(default_value, Field) else Field(default=default_value)
            fields.update({field_name: field(field_name, field_type)})
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
