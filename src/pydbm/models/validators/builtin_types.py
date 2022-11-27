import datetime
import typing

__all__ = (
    "validate_bool",
    "validate_bytes",
    "validate_date",
    "validate_datetime",
    "validate_dict",
    "validate_float",
    "validate_int",
    "validate_list",
    "validate_none",
    "validate_set",
    "validate_str",
    "validate_tuple",
)


def validate_bool(value: typing.Any) -> None:
    if not isinstance(value, bool):
        raise ValueError("It must be bool")


def validate_bytes(value: typing.Any) -> None:
    if not isinstance(value, bytes):
        raise ValueError("It must be bytes")


def validate_date(value: typing.Any) -> None:
    if not isinstance(value, datetime.date):
        raise ValueError("It must be date")


def validate_datetime(value: typing.Any) -> None:
    if not isinstance(value, datetime.datetime):
        raise ValueError("It must be datetime")


def validate_dict(value: typing.Any) -> None:
    if not isinstance(value, dict):
        raise ValueError("It must be dict")


def validate_float(value: typing.Any) -> None:
    if not isinstance(value, float):
        raise ValueError("It must be float")


def validate_int(value: typing.Any) -> None:
    if not isinstance(value, int):
        raise ValueError("It must be int")


def validate_list(value: typing.Any) -> None:
    if not isinstance(value, list):
        raise ValueError("It must be list")


def validate_none(value: typing.Any) -> None:
    if not isinstance(value, type(None)):
        raise ValueError("It must be None")


def validate_set(value: typing.Any) -> None:
    if not isinstance(value, set):
        raise ValueError("It must be set")


def validate_str(value: typing.Any) -> None:
    if not isinstance(value, str):
        raise ValueError("It must be str")


def validate_tuple(value: typing.Any) -> None:
    if not isinstance(value, tuple):
        raise ValueError("It must be tuple")
