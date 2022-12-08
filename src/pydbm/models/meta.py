from __future__ import annotations

import typing

from pydbm.database import Database
from pydbm.models.fields import AutoField, Field, Undefined

__all__ = (
    "Config",
    "Meta",
    "PRIMARY_KEY",
    "UNIQUE_TOGETHER",
    "generate_table_name",
    "get_config",
)


PRIMARY_KEY = "pk"
UNIQUE_TOGETHER = ()


def generate_table_name(cls_name: str) -> str:
    return f"{cls_name.lower()}s"


class Config(typing.NamedTuple):
    table_name: str
    unique_together: typing.Tuple[str, ...]


def get_config(cls_name: str, config: Config | None = None) -> Config:
    if config is not None:
        table_name = config.table_name if hasattr(config, "table_name") else generate_table_name(cls_name)
        unique_together = config.unique_together if hasattr(config, "unique_together") else UNIQUE_TOGETHER
    else:
        table_name = generate_table_name(cls_name)
        unique_together = UNIQUE_TOGETHER

    return Config(table_name, unique_together)


# @typing.dataclass_transform(kw_only_default=True, field_specifiers=(Field,))  # TODO: fix it
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
    ) -> type:  # noqa: E501
        if not [b for b in bases if isinstance(b, mcs)]:
            return super().__new__(mcs, cls_name, bases, namespace, **kwargs)

        config = get_config(cls_name, namespace.get("Config", None))

        fields = mcs.inspect_namespace(namespace, config)
        required_fields, not_required_fields = mcs.split_fields(list(fields.values()))

        slots = {field.private_name for field in fields.values()}

        namespace["__slots__"] = tuple(sorted(slots))
        namespace["required_fields"] = required_fields
        namespace["not_required_fields"] = not_required_fields
        namespace["database"] = Database(config.table_name)
        namespace.update(**fields)

        return super().__new__(mcs, cls_name, bases, namespace, **kwargs)

    def __call__(self, **kwargs):
        for field in self.not_required_fields:
            if field.public_name not in kwargs and field.public_name != PRIMARY_KEY:
                kwargs[field.public_name] = field.get_default_value()  # type: ignore[attr-defined]  # noqa: E501

        for field in self.required_fields:  # type: ignore[assignment]
            if field not in kwargs:
                raise ValueError(f"{field} is required")

        primary_key_field: AutoField | None = next(
            filter(
                lambda field: field.public_name not in kwargs and field.public_name == PRIMARY_KEY,  # type: ignore[arg-type]  # noqa: E501
                self.not_required_fields,
            ),
            None,
        )
        if primary_key_field:
            kwargs[primary_key_field.public_name] = primary_key_field(kwargs).get_default_value()  # type: ignore[attr-defined]  # noqa: E501

        return super().__call__(**kwargs)

    @classmethod
    def inspect_namespace(mcs, namespace: dict[str, typing.Any], config: Config) -> dict[str, Field | AutoField]:
        """Inspect namespace and return fields."""
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

        fields[PRIMARY_KEY] = AutoField("pk", "str", unique_together=config.unique_together or list(fields.keys()))  # type: ignore[arg-type]  # noqa: E501
        return fields

    @classmethod
    def split_fields(mcs, fields: list[Field | AutoField]) -> tuple[list[str], list[Field | AutoField]]:
        required_fields: list[str] = []
        not_required_fields: list[Field | AutoField] = []

        for field in fields:
            if field.is_required():
                required_fields.append(field.public_name)
            else:
                not_required_fields.append(field)
        return required_fields, not_required_fields
