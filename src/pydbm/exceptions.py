import typing

__all__ = (
    "BaseException",
    "DoesNotExists",
    "PydbmTypeError",
    "ValidationError",
)


class BaseException(Exception):
    """Base exception for pydbm models."""

    pass


class DoesNotExists(BaseException):
    """Exception for not found id in the models."""

    pass


class PydbmTypeError(BaseException, TypeError):
    """Exception for not valid type of value."""

    pass


class ValidationError(BaseException):
    """Exception for not valid value."""

    def __init__(self, field_name: str, field_value: typing.Any, error: ValueError) -> None:
        self.field_name = field_name
        self.field_value = field_value
        self.error = error

    def __str__(self) -> str:
        return f"Invalid value for {self.field_name}={self.field_value!r}; {self.error}."  # noqa: E501
