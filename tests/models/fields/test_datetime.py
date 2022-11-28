from pydbm import DateField, DateTimeField, validate_date, validate_datetime


def test_datetime_field_check_validator():
    field = DateTimeField()
    assert field.validators == [validate_datetime]


def test_date_field_check_validator():
    field = DateField()
    assert field.validators == [validate_date]
