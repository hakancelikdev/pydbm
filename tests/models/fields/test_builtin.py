from pydbm import (
    GenericField,
    validate_bool,
    validate_bytes,
    validate_dict,
    validate_float,
    validate_int,
    validate_list,
    validate_set,
    validate_str,
    validate_tuple,
)


def test_builtin_field_str_check_validator():
    field = GenericField(field_type=str)
    assert field.validators == [validate_str]


def test_builtin_field_int_check_validator():
    field = GenericField(field_type=int)
    assert field.validators == [validate_int]


def test_builtin_field_float_check_validator():
    field = GenericField(field_type=float)
    assert field.validators == [validate_float]


def test_builtin_field_bool_check_validator():
    field = GenericField(field_type=bool)
    assert field.validators == [validate_bool]


def test_builtin_field_list_check_validator():
    field = GenericField(field_type=list)
    assert field.validators == [validate_list]


def test_builtin_field_dict_check_validator():
    field = GenericField(field_type=dict)
    assert field.validators == [validate_dict]


def test_builtin_field_tuple_check_validator():
    field = GenericField(field_type=tuple)
    assert field.validators == [validate_tuple]


def test_builtin_field_set_check_validator():
    field = GenericField(field_type=set)
    assert field.validators == [validate_set]


def test_builtin_field_bytes_check_validator():
    field = GenericField(field_type=bytes)
    assert field.validators == [validate_bytes]
