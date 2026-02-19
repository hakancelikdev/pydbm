from __future__ import annotations

import inspect
import sys
import typing

__all__ = (
    "get_obj_annotations",
    "is_optional_type",
    "unwrap_optional",
)


def is_optional_type(tp: typing.Any) -> bool:
    """Check if a type is Optional (Union with NoneType), e.g. Optional[str] or str | None."""
    origin = typing.get_origin(tp)
    if origin is typing.Union:
        args = typing.get_args(tp)
        return type(None) in args and len(args) == 2
    if sys.version_info >= (3, 10):
        import types as _types

        if isinstance(tp, _types.UnionType):
            args = typing.get_args(tp)
            return type(None) in args and len(args) == 2
    return False


def unwrap_optional(tp: typing.Any) -> typing.Any:
    """Extract the inner type from Optional[X] / X | None."""
    args = typing.get_args(tp)
    for arg in args:
        if arg is not type(None):
            return arg
    return type(None)


def get_obj_annotations(*, obj: typing.Type[typing.Any]) -> dict[str, typing.Any]:
    assert inspect.isclass(obj), f"{obj!r} must be a class"

    globals_ = sys.modules[obj.__module__].__dict__
    locals_ = dict(vars(obj))

    if sys.version_info >= (3, 10):
        from inspect import get_annotations

        return get_annotations(obj, globals=globals_, locals=locals_, eval_str=True)

    ann = obj.__dict__.get("__annotations__", None) if isinstance(obj, type) else getattr(obj, "__annotations__", None)
    assert ann is not None, "No annotations found, please open an issue -> https://github.com/hakancelikdev/pydbm/issues/new"  # noqa

    return {
        key: value if not isinstance(value, str) else eval(value, globals_, locals_)
        for key, value in ann.items()
    }
