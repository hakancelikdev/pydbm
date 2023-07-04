from __future__ import annotations

import ast
import datetime
import dbm
import typing
from pathlib import Path

from pydbm.database.data_types import BaseDataType
from pydbm.inspect_extra import get_obj_annotations

if typing.TYPE_CHECKING:
    from pydbm import DbmModel
    from pydbm.typing_extra import SupportedClassT


__all__ = (
    "DATABASE_EXTENSION",
    "DATABASE_HEADER_MAPPING",
    "DATABASE_HEADER_NAME",
    "DATABASE_PATH",
    "DatabaseManager",
)

Self = typing.TypeVar("Self", bound="DatabaseManager")  # unexport: not-public

DATABASE_HEADER_NAME: str = "__database_headers__"
DATABASE_HEADER_MAPPING: dict[SupportedClassT, str] = {
    bool: "bool",
    bytes: "bytes",
    datetime.date: "date",
    datetime.datetime: "datetime",
    float: "float",
    int: "int",
    None: "null",
    str: "str",
}
DATABASE_EXTENSION: str = "pydbm"
DATABASE_PATH: Path = Path("pydbm")  # TODO: take from env


class DatabaseManager:
    if typing.TYPE_CHECKING:
        __database_headers__: dict[str, SupportedClassT]  # TODO: make this more generic

    __slots__ = (
        "model",
        "table_name",
        "db_path",
        "db",
        DATABASE_HEADER_NAME,
        "_keys",
    )

    def __init__(self, *, model: typing.Type[DbmModel], table_name: str) -> None:  # TODO: table_name -> db_name
        self.model = model
        self.table_name = table_name

        self.db_path = DATABASE_PATH / f"{self.table_name}.{DATABASE_EXTENSION}"

        ann = get_obj_annotations(obj=model)
        db_headers = bytes(str({key: DATABASE_HEADER_MAPPING[value] for key, value in ann.items()}), "utf-8")

        db = self.open()
        database_header: bytes | None
        if (database_header := db.get(DATABASE_HEADER_NAME, None)) is None:
            db[DATABASE_HEADER_NAME] = db_headers
        else:
            # TODO: migrations
            assert database_header == db_headers, f"Database headers are not equal: '{database_header}' != '{db_headers}'"  # type: ignore[str-bytes-safe]  # noqa: E501
        db.close()

        setattr(self, DATABASE_HEADER_NAME, ann)

    def __enter__(self, *args, **kwargs):
        return self.open()

    def __exit__(self, *args, **kwargs):
        self.close()

    def __len__(self) -> int:
        with self as db:
            return len(db) - 1  # NOTE: subtract 1 for the database header

    def __getitem__(self, pk: str) -> DbmModel:
        return self.get(pk=pk)

    def __setitem__(self, pk: str, fields: dict[str, typing.Any]) -> None:
        self.save(pk=pk, fields=fields)

    def __delitem__(self, pk: str) -> None:
        self.delete(pk=pk)

    def __contains__(self, pk: str) -> bool:
        with self as db:
            return pk in db

    def __iter__(self: Self) -> Self:
        with self as db:
            # TODO: take key one by one to improve performance
            self._keys: typing.Iterator[bytes] = iter(db.keys())
        return self

    def __next__(self) -> str:
        _key: bytes | None = next(self._keys, None)
        if _key is not None:
            key: str = _key.decode("utf-8")
            if key == DATABASE_HEADER_NAME:
                return next(self)
            return key
        else:
            del self._keys
            raise StopIteration

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model!r}, table_name={self.table_name!r})"

    def open(self):
        Path(DATABASE_PATH).mkdir(parents=True, exist_ok=True)

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

    def create(self, **kwargs) -> DbmModel:
        if not kwargs:
            raise ValueError("No fields provided")

        model = self.model(**kwargs)
        model.save()

        return model

    def get(self, *, pk: str) -> DbmModel:
        with self as db:
            data_from_dbm: bytes = db.get(pk, None)

        if data_from_dbm is not None:
            to_python = ast.literal_eval(data_from_dbm.decode("utf-8"))  # TODO: implement own parser
            fields: dict[str, typing.Any] = {"pk": pk}
            for key, value in to_python.items():
                fields[key] = BaseDataType.get_data_type(self.__database_headers__[key]).get(value)

            return self.model(**fields)

        raise self.model.DoesNotExists(f"{self.model.__name__} with pk {pk} does not exists")

    def update(self, *, pk: str, **updated_fields) -> None:
        model = self.get(pk=pk)
        fields = model.fields

        for key, value in updated_fields.items():
            fields[key] = value

        self.save(pk=pk, fields=fields)

    def delete(self, *, pk: str) -> None:
        with self as db:
            del db[pk]

    def all(self) -> typing.Iterable[DbmModel]:
        for key in self:
            yield self.get(pk=key)

    def filter(self, **kwargs) -> typing.Iterable[DbmModel]:
        def check(model: DbmModel) -> bool:
            return all(model.fields[key] == value for key, value in kwargs.items())

        yield from filter(check, self.all())

    def count(self):
        return len(self)
