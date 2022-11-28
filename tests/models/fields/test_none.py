from pydbm import NoneField, validate_none


def test_none_field_check_validator():
    field = NoneField()
    assert field.validators == [validate_none]
