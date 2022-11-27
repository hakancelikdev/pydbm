from pydbm.models.fields.sequence import BytesField, ListField, StrField, TupleField
from pydbm.models.validators import validate_bytes, validate_list, validate_str, validate_tuple


def test_str_field_check_validator():
    field = StrField()
    assert field.validators == [validate_str]

    field = StrField(max_value=10)
    assert len(field.validators) == 2  # TODO: Write this test explicitly

    field = StrField(max_value=10, min_value=5)
    assert len(field.validators) == 3  # TODO: Write this test explicitly


def test_bytes_field_check_validator():
    field = BytesField()
    assert field.validators == [validate_bytes]


def test_tuple_field_check_validator():
    field = TupleField()
    assert field.validators == [validate_tuple]

    field = TupleField(max_value=10)
    assert len(field.validators) == 2  # TODO: Write this test explicitly

    field = TupleField(max_value=10, min_value=5)
    assert len(field.validators) == 3  # TODO: Write this test explicitly


def test_list_field_check_validator():
    field = ListField()
    assert field.validators == [validate_list]

    field = ListField(max_value=10)
    assert len(field.validators) == 2  # TODO: Write this test explicitly

    field = ListField(max_value=10, min_value=5)
    assert len(field.validators) == 3  # TODO: Write this test explicitly
