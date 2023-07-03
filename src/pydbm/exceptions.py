# TODO: Add to docs.
import typing

__all__ = (
    "PydbmBaseException",
    "PydbmTypeError",
    "ValidationError",
    "EmptyModelError",
    "UnnecessaryParamsError",
)


class PydbmBaseException(Exception):
    """Base exception for pydbm models."""

    pass


class PydbmTypeError(PydbmBaseException, TypeError):
    """Exception for not valid type of value."""

    pass


class ValidationError(PydbmBaseException, ValueError):
    """Exception for not valid value."""

    def __init__(self, field_name: str, field_value: typing.Any, error: ValueError) -> None:
        self.field_name = field_name
        self.field_value = field_value
        self.error = error

    def __str__(self) -> str:
        return f"Invalid value for {self.field_name}={self.field_value!r}; {self.error}."


class EmptyModelError(PydbmBaseException):
    """Exception for empty model."""

    pass


class UnnecessaryParamsError(PydbmBaseException, ValueError):
    """Exception for invalid params."""

    pass
