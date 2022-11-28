from pydbm import BoolField, validate_bool


def test_bool_field_check_validator():
    field = BoolField()
    assert field.validators == [validate_bool]
