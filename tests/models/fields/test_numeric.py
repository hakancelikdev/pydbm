from pydbm.models.fields.numeric import FloatField, IntField
from pydbm.models.validators import validate_float, validate_int


def test_int_field_check_validator():
    field = IntField()
    assert field.validators == [validate_int]

    field = IntField(max_value=10)
    assert len(field.validators) == 2  # TODO: Write this test explicitly

    field = FloatField(max_value=10, min_value=5)
    assert len(field.validators) == 3  # TODO: Write this test explicitly


def test_float_field_check_validator():
    field = FloatField()
    assert field.validators == [validate_float]

    field = FloatField(max_value=10)
    assert len(field.validators) == 2  # TODO: Write this test explicitly

    field = FloatField(max_value=10, min_value=5)
    assert len(field.validators) == 3  # TODO: Write this test explicitly
