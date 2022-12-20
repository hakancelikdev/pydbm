from __future__ import annotations

import ast
import dbm
import typing
from pathlib import Path

from pydbm.database.data_types import BaseDataType
from pydbm.exceptions import DoesNotExists

__all__ = ["DatabaseManager", "DatabaseMeta"]

if typing.TYPE_CHECKING:
    from pydbm import BaseModel


class DatabaseMeta(type):
    __header_name__: typing.ClassVar[str] = "__database_headers__"

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)

        mcs = type(cls)

        model = kwargs.pop("model")
        headers, db_headers = mcs.get_headers(model=model)

        if mcs.__header_name__ not in instance:
            with instance as db:
                db[mcs.__header_name__] = db_headers
        else:
            with instance as db:
                # TODO: migrations
                assert db[mcs.__header_name__] == db_headers, f"Database headers are not equal: '{db[mcs.__header_name__]}' != '{db_headers}'"  # type: ignore[str-bytes-safe]  # noqa: E501

        instance.__database_headers__ = headers
        return instance

    @staticmethod
    def get_headers(model: typing.Type[BaseModel]) -> tuple[dict[str, str], bytes]:
        headers = {}
        for field_name, field_type_or_type_name in model.__annotations__.items():
            if isinstance(field_type_or_type_name, str):
                headers[field_name] = field_type_or_type_name
            else:
                headers[field_name] = field_type_or_type_name.__name__

        return headers, bytes(str(headers), "utf-8")


class DatabaseManager(metaclass=DatabaseMeta):
    if typing.TYPE_CHECKING:
        __database_headers__: dict[str, str]

    __slots__ = (
        "model",
        "table_name",
        "db_path",
        "db",
        "__database_headers__",
    )

    database_path: typing.ClassVar[Path] = Path("pydbm")  # TODO: take from env

    def __init__(self, *, model: typing.Type[BaseModel], table_name: str) -> None:  # TODO: table_name -> db_name
        self.model = model
        self.table_name = table_name

        self.db_path = self.database_path / f"{self.table_name}.db"

    def __enter__(self, *args, **kwargs):
        return self.open()

    def __exit__(self, *args, **kwargs):
        self.close()

    def __len__(self) -> int:
        with self as db:
            return len(db)

    def __getitem__(self, pk: str) -> BaseModel:
        return self.get(pk=pk)

    def __setitem__(self, pk: str, fields: dict[str, typing.Any]) -> None:
        self.save(pk=pk, fields=fields)

    def __delitem__(self, pk: str) -> None:
        self.delete(pk=pk)

    def __contains__(self, pk: str) -> bool:
        with self as db:
            return pk in db

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model!r}, table_name={self.table_name!r})"

    def open(self):
        Path(self.database_path).mkdir(parents=True, exist_ok=True)

        self.db = dbm.open(self.db_path.as_posix(), "c")
        return self.db

    def close(self):
        self.db.close()
        del self.db

    def save(self, *, pk: str, fields: dict[str, typing.Any]) -> None:
        data: dict[str, typing.Any] = {
            key: BaseDataType.get_data_type(self.__database_headers__[key]).set(value) for key, value in fields.items()
        }
        data_for_dbm = bytes(str(data), "utf-8")

        with self as db:
            db[pk] = data_for_dbm

    def create(self, **kwargs) -> BaseModel:
        if not kwargs:
            raise ValueError("No fields provided")

        model = self.model(**kwargs)
        model.save()

        return model

    def get(self, *, pk: str) -> BaseModel:
        with self as db:
            data_from_dbm: bytes = db.get(pk, None)

        if data_from_dbm is not None:
            to_python = ast.literal_eval(data_from_dbm.decode("utf-8"))  # TODO: implement own parser
            fields: dict[str, typing.Any] = {"pk": pk}
            for key, value in to_python.items():
                fields[key] = BaseDataType.get_data_type(self.__database_headers__[key]).get(value)

            return self.model(**fields)

        raise DoesNotExists(f"{self.model.__name__} with pk {pk} does not exists")

    def update(self, *, pk: str, **updated_fields) -> None:
        model = self.get(pk=pk)
        fields = model.fields

        for key, value in updated_fields.items():
            fields[key] = value

        self.save(pk=pk, fields=fields)

    def delete(self, *, pk: str) -> None:
        with self as db:
            del db[pk]

    def keys(self) -> list[str]:
        with self as db:
            keys = list(db.keys())[1:]

        return keys

    def all(self) -> typing.Iterable[BaseModel]:
        for key in self.keys():
            yield self.get(pk=key)

    def filter(self, **kwargs) -> typing.Iterable[BaseModel]:
        def check(model: BaseModel) -> bool:
            return all(model.fields[key] == value for key, value in kwargs.items())

        yield from filter(check, self.all())
