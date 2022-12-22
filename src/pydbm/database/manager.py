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
    "DatabaseManager",
)

Self = typing.TypeVar("Self", bound="DatabaseManager")  # unexport: not-public


class DatabaseManager:
    if typing.TYPE_CHECKING:
        __database_headers__: dict[str, SupportedClassT]  # TODO: make this more generic

    __header_name__: typing.ClassVar[str] = "__database_headers__"
    __header_mapping__: dict[SupportedClassT, str] = {
        bool: "bool",
        bytes: "bytes",
        datetime.date: "date",
        datetime.datetime: "datetime",
        float: "float",
        int: "int",
        None: "null",
        str: "str",
    }

    __slots__ = (
        "model",
        "table_name",
        "db_path",

        "db",
        __header_name__,

        "__key",
    )

    database_path: typing.ClassVar[Path] = Path("pydbm")  # TODO: take from env

    def __init__(self, *, model: typing.Type[DbmModel], table_name: str) -> None:  # TODO: table_name -> db_name
        self.model = model
        self.table_name = table_name

        self.db_path = self.database_path / f"{self.table_name}.db"

        ann = get_obj_annotations(obj=model)
        db_headers = bytes(str({key: self.__class__.__header_mapping__[value] for key, value in ann.items()}), "utf-8")

        db = self.open()
        first_key: bytes | None = db.firstkey()
        if first_key is None:
            db[self.__class__.__header_name__] = db_headers
        else:
            assert first_key == self.__class__.__header_name__.encode(), f"First key is not {self.__class__.__header_name__}"  # noqa: E501
            # TODO: migrations
            assert db[first_key] == db_headers, f"Database headers are not equal: '{db[self.__class__.__header_name__]}' != '{db_headers}'"  # type: ignore[str-bytes-safe]  # noqa: E501
        db.close()

        setattr(self, self.__class__.__header_name__, ann)

    def __enter__(self, *args, **kwargs):
        return self.open()

    def __exit__(self, *args, **kwargs):
        self.close()

    def __len__(self) -> int:
        with self as db:
            return len(db)

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
        self.__key: bytes = self.__class__.__header_name__.encode()  # NOTE: this is the first key in the database
        return self

    def __next__(self) -> str:
        with self as db:
            self.__key: bytes | None = db.nextkey(self.__key)  # type: ignore

        if self.__key is not None:
            return self.__key.decode("utf-8")
        else:
            del self.__key
            raise StopIteration

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
