import pytest

from pydbm import Field, Undefined, ValidationError, validate_str


def test_base_attributes_with_call():
    field = Field()("field", str)

    assert repr(field) == f"Field('field', {str!r})"
    assert str(field) == f"Field('field', {str!r})"

    assert field.default == Undefined
    assert field.default_factory == Undefined
    assert field.get_default_value() is None
    assert field.field_name == "field"
    assert field.field_type == str
    assert field.is_required() is True
    assert field.normalizers == []
    assert field.private_name == "_field"
    assert field.public_name == "field"
    assert field.validators == [validate_str]


def test_base_attributes():
    field = Field()

    assert repr(field) == "Field(default=Undefined, default_factory=Undefined, normalizers=[], validators=[])"
    assert str(field) == "Field(default=Undefined, default_factory=Undefined, normalizers=[], validators=[])"

    assert field.default == Undefined
    assert field.default_factory == Undefined
    assert field.get_default_value() is None
    assert field.is_required() is True
    assert field.normalizers == []
    assert field.validators == []


def test_base_set_attr():
    class Model:
        field = Field()("field", str)

    model = Model()

    model.field = "value"  # set
    assert model.field == "value"  # get


def test_base_is_required():
    field = Field()
    assert field.is_required() is True

    field = Field(default=True)
    assert field.is_required() is False

    field = Field(default_factory=list)
    assert field.is_required() is False


def test_base_default_mutually_exclusive():
    with pytest.raises(AssertionError) as cm:
        Field(default=True, default_factory=list)
    assert str(cm.value) == "default and default_factory are mutually exclusive"


def test_base_validator_not_raise_value_error():
    class Model:
        field = Field(validators=[lambda value: False])("field", str)

    with pytest.raises(ValidationError) as cm:
        Model().field = "test"
    assert str(cm.value) == "Invalid value for field='test'; Value is not valid."
