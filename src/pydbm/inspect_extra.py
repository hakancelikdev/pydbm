from __future__ import annotations

import inspect
import sys
import typing

__all__ = (
    "get_obj_annotations",
)


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
