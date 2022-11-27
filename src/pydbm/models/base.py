from __future__ import annotations

import typing

from pydbm.database import Database
from pydbm.models.meta import Meta

__all__ = ("BaseModel",)


class BaseModel(metaclass=Meta):
    # TODO: we can not use id and pk, fix it
    if typing.TYPE_CHECKING:
        required_fields: typing.ClassVar[list[str]]
        database: typing.ClassVar[Database]
        pk: str
        id: str

    __slots__ = ("fields", "id")

    def __init__(self, **fields: typing.Any) -> None:
        self.id = fields.pop("pk")

        self.fields: dict[str, typing.Any] = fields

        for key, value in fields.items():
            setattr(self, key, value)

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

    def save(self) -> None:
        with self.database.db as db:
            db[self.pk] = self.fields | {"pk": self.pk}

    @classmethod
    def create(cls, **kwargs) -> BaseModel:  # TODO: add annotation
        if not kwargs:
            raise ValueError("No fields provided")

        model = cls(**kwargs)
        model.save()

        return cls.get(model.id)

    @classmethod
    def get(cls, id: str, default: typing.Any | None = None) -> BaseModel | None:  # TODO: add annotation
        with cls.database.db as db:
            data = db.get(id, default)
        if data is None:
            return None

        return cls(**data)

    def delete(self) -> None:
        with self.database.db as db:
            del db[self.pk]

    def update(self, **updated_fields) -> None:
        for key, value in updated_fields.items():
            self.fields[key] = value
            setattr(self, key, value)

        self.save()

    @classmethod
    def all(cls) -> typing.Iterator[BaseModel]:
        with cls.database.db as db:
            keys = db.keys()

        for key in keys:
            yield cls.get(key)

    @classmethod
    def filter(cls, **filters) -> typing.Iterator[BaseModel]:
        for model in cls.all():
            if all(getattr(model, key) == value for key, value in filters.items()):
                yield model
