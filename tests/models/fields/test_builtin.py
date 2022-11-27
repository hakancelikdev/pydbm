from pydbm.models import validators
from pydbm.models.fields.generic import GenericField


def test_builtin_field_str_check_validator():
    field = GenericField(field_type=str)
    assert field.validators == [validators.validate_str]


def test_builtin_field_int_check_validator():
    field = GenericField(field_type=int)
    assert field.validators == [validators.validate_int]


def test_builtin_field_float_check_validator():
    field = GenericField(field_type=float)
    assert field.validators == [validators.validate_float]


def test_builtin_field_bool_check_validator():
    field = GenericField(field_type=bool)
    assert field.validators == [validators.validate_bool]


def test_builtin_field_list_check_validator():
    field = GenericField(field_type=list)
    assert field.validators == [validators.validate_list]


def test_builtin_field_dict_check_validator():
    field = GenericField(field_type=dict)
    assert field.validators == [validators.validate_dict]


def test_builtin_field_tuple_check_validator():
    field = GenericField(field_type=tuple)
    assert field.validators == [validators.validate_tuple]


def test_builtin_field_set_check_validator():
    field = GenericField(field_type=set)
    assert field.validators == [validators.validate_set]


def test_builtin_field_bytes_check_validator():
    field = GenericField(field_type=bytes)
    assert field.validators == [validators.validate_bytes]
