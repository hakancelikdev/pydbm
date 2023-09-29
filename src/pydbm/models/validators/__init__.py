import datetime

from pydbm.models.validators.array import validate_array_float, validate_array_int, validate_array_str
from pydbm.models.validators.builtin_types import (
    validate_bool,
    validate_bytes,
    validate_date,
    validate_datetime,
    validate_float,
    validate_int,
    validate_none,
    validate_str,
)
from pydbm.models.validators.compare import validate_max_value, validate_min_value
from pydbm.typing_extra import array

__all__ = (
    "validate_bool",
    "validate_bytes",
    "validate_date",
    "validate_datetime",
    "validate_float",
    "validate_int",
    "validate_max_value",
    "validate_min_value",
    "validate_none",
    "validate_array_int",
    "validate_array_float",
    "validate_array_str",
    "validate_str",
    "VALIDATOR_MAPPING",
)


VALIDATOR_MAPPING = {
    bool: validate_bool,
    bytes: validate_bytes,
    datetime.date: validate_date,
    datetime.datetime: validate_datetime,
    float: validate_float,
    int: validate_int,
    None: validate_none,
    str: validate_str,
    array[int]: validate_array_int,
    array[float]: validate_array_float,
    array[str]: validate_array_str,
}
