from __future__ import annotations

import array as build_in_array
import datetime
import typing

__all__ = [
    "ArrayT",
    "NormalizationT",
    "SupportedClassT",
    "TYPE_TO_TYPECODE",
    "ValidatorT",
    "array",
    "dataclass_transform",
]


ArrayT = typing.TypeVar("ArrayT")
NormalizationT = typing.Callable[[typing.Any], typing.Any]
ValidatorT = typing.Callable[[typing.Any], typing.Optional[bool]]
TYPE_TO_TYPECODE: typing.Final[dict[typing.Type[int | float | str], typing.Literal["q", "d", "u"]]] = {
    int: "q",
    float: "d",
    str: "u",
}


def dataclass_transform(
    *,
    eq_default: bool = True,
    order_default: bool = False,
    kw_only_default: bool = False,
    field_specifiers: tuple[typing.Type[typing.Any] | typing.Callable[..., typing.Any], ...] = (),
    **kwargs: typing.Any,
) -> typing.Callable[[typing.Any], typing.Any]:
    """Here is the source code ->
    https://github.com/python/cpython/blob/v3.11.0/Lib/typing.py#L3343."""

    def decorator(cls_or_fn):
        cls_or_fn.__dataclass_transform__ = {
            "eq_default": eq_default,
            "order_default": order_default,
            "kw_only_default": kw_only_default,
            "field_specifiers": field_specifiers,
            "kwargs": kwargs,
        }
        return cls_or_fn

    return decorator


class array(build_in_array.array, typing.Generic[ArrayT]):
    if typing.TYPE_CHECKING:
        array_type: typing.Type[int | float | str]

    def __new__(cls, *initializer: int | float | str) -> array[ArrayT]:
        first_element_class = initializer[0].__class__
        typecode = TYPE_TO_TYPECODE.get(first_element_class)
        if typecode is None:
            raise TypeError(f"Only int, float, str are supported, but got {first_element_class.__name__}")

        if first_element_class is str:
            obj = super().__new__(cls, typecode, "".join(initializer))  # type: ignore[call-arg,arg-type]
        else:
            obj = super().__new__(cls, typecode, list(initializer))  # type: ignore[call-arg]

        obj.array_type = first_element_class
        return obj

    def __repr__(self):
        initializer = ", ".join(map(repr, self))
        return f"array({initializer})"


SupportedClassT = typing.Union[
    typing.Type[bool],
    typing.Type[bytes],
    typing.Type[datetime.date],
    typing.Type[datetime.datetime],
    typing.Type[float],
    typing.Type[int],
    typing.Type[None],
    typing.Type[str],
    typing.Type[array],
    typing.Type[array[int]],
    typing.Type[array[float]],
    typing.Type[array[str]],
]
