from __future__ import annotations

import ast
import datetime
import dbm
import typing
from pathlib import Path

from pydbm import contstant as C
from pydbm.database.data_types import BaseDataType
from pydbm.inspect_extra import get_obj_annotations
from pydbm.models.fields import AutoField

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
        "__is_db_open",
    )

    def __init__(self, *, model: typing.Type[DbmModel], table_name: str) -> None:  # TODO: table_name -> db_name
        self.model = model
        self.table_name = table_name

        self.__is_db_open: bool = False
        Path(DATABASE_PATH).mkdir(parents=True, exist_ok=True)
        self.db_path = (DATABASE_PATH / f"{self.table_name}.{DATABASE_EXTENSION}").as_posix()

        self.set_database_header()

    def __enter__(self, *args, **kwargs):
        return self.open()

    def __exit__(self, *args, **kwargs):
        self.close()

    def __len__(self) -> int:
        with self as db:
            return len(db) - 1  # NOTE: subtract 1 for the database header

    def __getitem__(self, id: str) -> DbmModel:
        return self.get(id=id)

    def __setitem__(self, id: str, fields: dict[str, typing.Any]) -> None:
        self.save(id=id, fields=fields)

    def __delitem__(self, id: str) -> None:
        self.delete(id=id)

    def __contains__(self, id: str) -> bool:
        with self as db:
            return id in db

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

    def set_database_header(self):
        ann = get_obj_annotations(obj=self.model)
        db_headers = bytes(str({key: DATABASE_HEADER_MAPPING[value] for key, value in ann.items()}), "utf-8")

        with self as db:
            database_header: bytes | None
            if (database_header := db.get(DATABASE_HEADER_NAME, None)) is None:
                db[DATABASE_HEADER_NAME] = db_headers

        if database_header is not None:
            # TODO: migrations
            assert database_header == db_headers, f"Database headers are not equal: '{database_header}' != '{db_headers}'"  # type: ignore[str-bytes-safe]  # noqa: E501

        setattr(self, DATABASE_HEADER_NAME, ann)

    def open(self):
        if not self.__is_db_open:
            self.db = dbm.open(self.db_path, "c")
            self.__is_db_open = True
        return self.db

    def close(self) -> None:
        if self.__is_db_open:
            self.db.close()
            self.__is_db_open = False

    def save(self, *, id: str, fields: dict[str, typing.Any]) -> None:
        data: dict[str, typing.Any] = {
            key: BaseDataType.get_data_type(self.__database_headers__[key]).set(value) for key, value in fields.items()
        }
        data_for_dbm = bytes(str(data), "utf-8")

        with self as db:
            db[id] = data_for_dbm

    def create(self, **kwargs) -> DbmModel:
        if not kwargs:
            raise ValueError("No fields provided")

        model = self.model(**kwargs)
        model.save()

        return model

    def get(self, *, id: str | None = None, **unique_together) -> DbmModel:
        if id is None:
            if self.model._config.unique_together != tuple(unique_together.keys()):
                raise self.model.RiskofReturningMultipleObjects(
                    "To get single data from database you must pass"
                    f" all unique_together fields: {self.model._config.unique_together}"
                )

            auto_field = AutoField(
                field_name=C.PRIMARY_KEY,
                field_type=str,
                unique_together=self.model._config.unique_together
            )
            id = auto_field(fields=unique_together).get_default_value()

        with self as db:
            data_from_dbm: bytes = db.get(id, None)

        if data_from_dbm is not None:
            to_python = ast.literal_eval(data_from_dbm.decode("utf-8"))  # TODO: implement own parser
            fields: dict[str, typing.Any] = {}
            for key, value in to_python.items():
                fields[key] = BaseDataType.get_data_type(self.__database_headers__[key]).get(value)

            return self.model(**fields)

        if id is None:
            raise self.model.DoesNotExists(f"{self.model.__name__} with {unique_together} does not exists")
        else:
            raise self.model.DoesNotExists(f"{self.model.__name__} with id {id} does not exists")

    def update(self, *, id: str, **updated_fields) -> None:
        model = self.get(id=id)
        fields = model.fields

        for key, value in updated_fields.items():
            fields[key] = value

        self.save(id=id, fields=fields)

    def delete(self, *, id: str) -> None:
        with self as db:
            del db[id]

    def all(self) -> typing.Iterable[DbmModel]:
        for key in self:
            yield self.get(id=key)

    def filter(self, **kwargs) -> typing.Iterator[DbmModel]:
        def check(model: DbmModel) -> bool:
            return all(model.fields[key] == value for key, value in kwargs.items())

        yield from filter(check, self.all())

    def exists(self, **kwargs) -> bool:
        if (id := kwargs.pop(C.PRIMARY_KEY, None)) is None and self.model._config.unique_together == tuple(kwargs.keys()):  # noqa: E501
            auto_field = AutoField(
                field_name=C.PRIMARY_KEY,
                field_type=str,
                unique_together=self.model._config.unique_together
            )
            id = auto_field(fields=kwargs).get_default_value()

        if id is not None:
            with self as db:
                data_from_dbm: bytes = db.get(id, None)
            return data_from_dbm is not None
        else:
            return not (next(self.filter(**kwargs), False) is False)

    def count(self):
        return len(self)
