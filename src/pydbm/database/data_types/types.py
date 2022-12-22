from __future__ import annotations

import datetime

from pydbm.database.data_types.base import BaseDataType

__all__ = (
    "BoolDataType",
    "BytesDataType",
    "DateDataType",
    "DateTimeDataType",
    "FloatDataType",
    "IntDataType",
    "NoneDataType",
    "StrDataType",
)


class BoolDataType(BaseDataType, data_type=bool):
    mapping = {
        "True": True,
        "False": False,
    }

    @classmethod
    def get(cls, value: str) -> bool:
        return cls.mapping[value]

    @staticmethod
    def set(value: bool) -> str:
        return str(value)


class BytesDataType(BaseDataType, data_type=bytes):
    @classmethod
    def get(cls, value: str) -> bytes:
        return bytes(value, "utf-8")

    @staticmethod
    def set(value: bytes) -> str:
        return value.decode("utf-8")


class DateDataType(BaseDataType, data_type=datetime.date):
    @classmethod
    def get(cls, value: str) -> datetime.date:
        return datetime.date.fromisoformat(value)

    @staticmethod
    def set(value: datetime.date) -> str:
        return value.isoformat()


class DateTimeDataType(BaseDataType, data_type=datetime.datetime):
    @classmethod
    def get(cls, value: str) -> datetime.date:
        return datetime.datetime.fromisoformat(value)

    @staticmethod
    def set(value: datetime.datetime) -> str:
        return value.isoformat()


class FloatDataType(BaseDataType, data_type=float):
    @classmethod
    def get(cls, value: str) -> float:
        return float(value)

    @staticmethod
    def set(value: float) -> str:
        return str(value)


class IntDataType(BaseDataType, data_type=int):
    @classmethod
    def get(cls, value: str) -> int:
        return int(value)

    @staticmethod
    def set(value: int) -> str:
        return str(value)


class NoneDataType(BaseDataType, data_type=None):
    @classmethod
    def get(cls, value: str) -> None:
        return None

    @staticmethod
    def set(value: None) -> str:
        return str(value)


class StrDataType(BaseDataType, data_type=str):
    @classmethod
    def get(cls, value: str) -> str:
        return value

    @staticmethod
    def set(value: str) -> str:
        return str(value)
