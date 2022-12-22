import datetime

import pytest

from pydbm.inspect_extra import get_obj_annotations


def test_get_obj_annotations_not_class():
    def foo(p: int):
        pass

    with pytest.raises(AssertionError):
        get_obj_annotations(obj=foo)


@pytest.mark.parametrize("type_, expected_type", [
    (bool, bool),
    (bytes, bytes),
    (datetime.date, datetime.date),
    (datetime.datetime, datetime.datetime),
    (float, float),
    (int, int),
    (str, str),
    (None, None),
    ("bool", bool),
    ("bytes", bytes),
    ("datetime.date", datetime.date),
    ("datetime.datetime", datetime.datetime),
    ("float", float),
    ("int", int),
    ("str", str),
    ("None", None),
])
def test_get_obj_annotations(type_, expected_type):
    # Normal class
    obj = type("o", (), {"__annotations__": {"t": type_}})
    assert get_obj_annotations(obj=obj) == {"t": expected_type}

    # DbmModel
    # TODO: https://github.com/hakancelikdev/pydbm/issues/25
    # obj = type("o", (DbmModel,), {"__annotations__": {"t": type_}})
    # assert get_obj_annotations(obj=obj) == {"t": expected_type}
