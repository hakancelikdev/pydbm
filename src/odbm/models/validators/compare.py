import typing

__all__ = (
    "validate_max_value",
    "validate_min_value",
)


def validate_max_value(max_value: int) -> typing.Callable[[typing.Any], None]:
    def check_max_value(value: typing.Any):
        if value > max_value:
            raise ValueError(f"{value!r} must be less than {max_value}")

    return check_max_value


def validate_min_value(min_value: int) -> typing.Callable[[typing.Any], None]:
    def check_min_value(value: typing.Any):
        if value < min_value:
            raise ValueError(f"{value!r} must be greater than {min_value}")

    return check_min_value
