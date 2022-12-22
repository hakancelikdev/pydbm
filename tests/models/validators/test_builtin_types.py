import datetime

import pytest

from pydbm.models.validators import builtin_types


@pytest.mark.parametrize(
    "validator_name, value",
    [
        ("validate_bool", True),
        ("validate_bool", False),
        ("validate_bytes", b""),
        ("validate_date", datetime.date.today()),
        ("validate_datetime", datetime.datetime.now()),
        ("validate_float", 1.0),
        ("validate_int", 1),
        ("validate_none", None),
        ("validate_str", ""),
    ],
)
def test_builtin_types_valid(validator_name, value):
    validator = getattr(builtin_types, validator_name)
    assert validator(value) is None


@pytest.mark.parametrize(
    "validator_name, value, exception_msg",
    [
        ("validate_bool", 1, "It must be bool"),
        ("validate_bool", 0, "It must be bool"),
        ("validate_bytes", 1, "It must be bytes"),
        ("validate_date", 1, "It must be date"),
        ("validate_datetime", 1, "It must be datetime"),
        ("validate_float", 1, "It must be float"),
        ("validate_int", 1.1, "It must be int"),
        ("validate_none", 1, "It must be None"),
        ("validate_str", 1, "It must be str"),
    ],
)
def test_builtin_types_invalid(validator_name, value, exception_msg):
    validator = getattr(builtin_types, validator_name)
    with pytest.raises(ValueError) as cm:
        validator(value)
    assert str(cm.value) == exception_msg
