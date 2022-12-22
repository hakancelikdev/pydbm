from __future__ import annotations

import typing

from pydbm.database import DatabaseManager
from pydbm.models.meta import Meta

__all__ = (
    "DbmModel",
)


class DbmModel(metaclass=Meta):
    if typing.TYPE_CHECKING:
        required_fields: typing.ClassVar[list[str]]
        objects: typing.ClassVar[DatabaseManager]
        pk: str
        id: str

    def __init__(self, **fields: typing.Any) -> None:
        self.id = fields.pop("pk")

        self.fields: dict[str, typing.Any] = fields

        for key, value in fields.items():
            setattr(self, key, value)

    def save(self) -> None:
        self.objects.save(pk=self.pk, fields=self.fields)

    def update(self, **updated_fields) -> None:
        for field_name, field_value in updated_fields.items():
            setattr(self, field_name, field_value)

        self.objects.update(pk=self.pk, **updated_fields)

    def delete(self) -> None:
        self.objects.delete(pk=self.pk)

    def as_dict(self) -> dict[str, typing.Any]:
        return self.fields

    def __repr__(self):
        kwargs = ", ".join(f"{key}={getattr(self, key)!r}" for key in self.fields)
        return f"{type(self).__name__}({kwargs})"

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.fields == other.fields and self.pk == other.pk
        return False

    def __hash__(self):
        if self.pk is None:
            raise TypeError("Model instances without primary key value are unhashable")
        return hash(self.pk)
