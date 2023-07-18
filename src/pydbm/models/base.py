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
        empty_model: typing.ClassVar[bool]
        id: str

    def __init__(self, **fields: typing.Any) -> None:
        self.fields: dict[str, typing.Any] = {}
        for key, value in fields.items():
            setattr(self, key, value)

    def __repr__(self):
        kwargs = ", ".join(f"{key}={getattr(self, key)!r}" for key in self.fields)
        return f"{type(self).__name__}({kwargs})"

    def __eq__(self, other):
        if isinstance(other, type(self)):
            for key, value in self.fields.items():
                if getattr(other, key) != value:
                    break
            else:
                return self.id == other.id
        return False

    def __hash__(self):
        if self.id is None:
            raise TypeError("Model instances without primary key value are unhashable")
        return hash(self.id)

    def __len__(self):
        return self.objects.count()  # type: ignore

    def save(self) -> None:
        self.objects.save(id=self.id, fields=self.fields)

    def update(self, **updated_fields) -> None:
        for field_name, field_value in updated_fields.items():
            setattr(self, field_name, field_value)

        self.objects.update(id=self.id, **updated_fields)

    def delete(self) -> None:
        self.objects.delete(id=self.id)

    def as_dict(self) -> dict[str, typing.Any]:
        return self.fields
