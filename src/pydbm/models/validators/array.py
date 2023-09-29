import typing

from pydbm.typing_extra import array

__all__ = (
    "validate_array_float",
    "validate_array_int",
    "validate_array_str",
)


def validate_array_int(value: typing.Any) -> None:
    if value.__class__ is not array:
        raise ValueError("It must be array")
    if value.array_type is not int:
        raise ValueError("It must be array[int]")


def validate_array_str(value: typing.Any) -> None:
    if value.__class__ is not array:
        raise ValueError("It must be array")
    if value.array_type is not str:
        raise ValueError("It must be array[str]")


def validate_array_float(value: typing.Any) -> None:
    if value.__class__ is not array:
        raise ValueError("It must be array")
    if value.array_type is not float:
        raise ValueError("It must be array[float]")
