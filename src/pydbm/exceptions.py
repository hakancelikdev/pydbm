import typing

__all__ = (
    "OdbmBaseException",
    "DoesNotExists",
    "OdbmTypeError",
    "OdbmValidationError",
)


class OdbmBaseException(Exception):
    """Base exception for pydbm models."""

    pass


class DoesNotExists(OdbmBaseException):
    """Exception for not found id in the models."""

    pass


class OdbmTypeError(OdbmBaseException, TypeError):
    """Exception for not valid type of value."""

    pass


class OdbmValidationError(OdbmBaseException):
    """Exception for not valid value."""

    def __init__(self, field_name: str, field_value: typing.Any, error: ValueError) -> None:
        self.field_name = field_name
        self.field_value = field_value
        self.error = error

    def __str__(self) -> str:
        return f"Invalid value for {self.field_name}={self.field_value!r}; {self.error}, not {type(self.field_value).__name__}"  # noqa: E501
