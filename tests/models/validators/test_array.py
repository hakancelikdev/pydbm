
import pytest

from pydbm.models import validators
from pydbm.typing_extra import array


@pytest.mark.parametrize(
    "validator_name, value",
    [
        ("validate_array_float", array(1.1, 2.2)),
        ("validate_array_int", array(1, 2)),
        ("validate_array_str", array("a", "b")),
    ],
)
def test_builtin_types_valid(validator_name, value):
    validator = getattr(validators, validator_name)
    assert validator(value) is None


@pytest.mark.parametrize(
    "validator_name, value, exception_msg",
    [
        ("validate_array_float", [1, 2], "It must be array"),
        ("validate_array_int", [1.2, 2.1], "It must be array"),
        ("validate_array_str", [1, 2], "It must be array"),
        ("validate_array_float", array(1, 2), "It must be array[float]"),
        ("validate_array_int", array(1.2, 2.1), "It must be array[int]"),
        ("validate_array_str", array(1, 2), "It must be array[str]"),
    ],
)
def test_builtin_types_invalid(validator_name, value, exception_msg):
    validator = getattr(validators, validator_name)
    with pytest.raises(ValueError) as cm:
        validator(value)
    assert str(cm.value) == exception_msg
