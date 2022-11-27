from __future__ import annotations

import ast
import contextlib
import dbm
import os
import typing
from pathlib import Path
from typing import Any, Literal

from pydbm.logging import logger

__all__ = ["DB_NAME", "Database", "DatabaseOperations"]

DB_NAME = "pydbm.db"


class DatabaseOperations:
    __slots__ = (
        "db",
        "table_name",
    )

    def __init__(self, db, table_name) -> None:
        self.db = db
        self.table_name = bytes(table_name, "utf-8")

    def __getitem__(self, key: str) -> bytes:
        return self.as_dict()[key]

    def __setitem__(self, key: str, value: typing.Any) -> None:
        if self.table_name in self.db:  # TODO: improve this approach, do not update every time all table
            table_dict = self.as_dict()
            table_dict[key] = value
            self.db[self.table_name] = bytes(str(table_dict), "utf-8")
        else:
            self.db[self.table_name] = bytes(str({key: value}), "utf-8")

    def __delitem__(self, key: str) -> None:
        table_dict = self.as_dict()
        table_dict.pop(key)
        self.db[self.table_name] = bytes(str(table_dict), "utf-8")

    def __contains__(self, key: str) -> bool:
        return bytes(key, "utf-8") in self.db[self.table_name]

    def __len__(self) -> int:
        try:
            return len(self.as_dict())
        except KeyError:
            return 0

    def keys(self):
        return list(self.as_dict().keys())

    def as_dict(self) -> dict:
        table = self.db[self.table_name]
        table_dict = ast.literal_eval(table.decode("unicode_escape"))
        return table_dict

    def get(self, key: str, default: Any = None) -> dict | Any:
        table_dict = self.as_dict()
        return table_dict.get(key, default)


class Database:  # TODO: bu class namespace'i olsa nasıl olur ?
    __slots__ = (
        "table_name",
        "db_path",
        "folder_path",
    )

    DB_PATH: str = "db/"  # TODO: take from env

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.db_path: Path = Path(f"{self.DB_PATH}{DB_NAME}")
        self.folder_path: str = os.sep.join(self.db_path.as_posix().split(os.sep)[:-1])

    def open(self, flag: Literal["r", "w", "c", "n"] = "c"):
        Path(self.folder_path).mkdir(parents=True, exist_ok=True)

        try:
            return dbm.open(self.db_path.as_posix(), flag=flag)
        except dbm.error as exc:
            logger.error(exc)  # TODO: open already opened db

    @property
    @contextlib.contextmanager
    def db(self) -> typing.Iterator[DatabaseOperations]:
        db_ = self.open()
        yield DatabaseOperations(db_, self.table_name)
        db_.close()

    def remove(self) -> None:
        self.db_path.with_suffix(".db").unlink()
        Path(self.folder_path).rmdir()
