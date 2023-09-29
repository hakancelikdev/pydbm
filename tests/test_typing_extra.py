import array as build_in_array
import sys

import pytest

from pydbm.typing_extra import array


@pytest.mark.parametrize("actual_array, expected_array", [
    (array(1, 2, 3), build_in_array.array("q", [1, 2, 3])),
    (array("a", "b", "c"), build_in_array.array("u", ["a", "b", "c"])),
    (array("a", "b", "c"), build_in_array.array("u", "abc")),
    (array(1.1, 2.2, 3.3), build_in_array.array("d", [1.1, 2.2, 3.3])),
    (array("abc"), build_in_array.array("u", ["a", "b", "c"])),
    (array("abc", "dfg"), build_in_array.array("u", "abcdfg")),
])
def test_array(actual_array, expected_array):
    assert actual_array == expected_array


@pytest.mark.parametrize(
    "value_type, value",
    [
        (float, array(1.1, 2.2)),
        (int, array(1, 2)),
        (str, array("a", "b")),
    ],
)
def test_array_type(value_type, value):
    assert value.array_type is value_type


def test_array_not_valid():
    with pytest.raises(TypeError) as cm:
        assert array(b"1", b"2", b"3")
    assert str(cm.value) == "Only int, float, str are supported, but got bytes"


def test_second_argument_not_valid():
    with pytest.raises(TypeError) as cm:
        assert array(1, "a")

    if sys.version_info >= (3, 10):
        assert str(cm.value) == "'str' object cannot be interpreted as an integer"
    else:
        assert str(cm.value) == "an integer is required (got type str)"
