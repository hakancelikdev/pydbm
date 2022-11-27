import pytest

from pydbm.models.fields.base import BaseField, Undefined
from pydbm.models.validators import validate_str


def test_base_attributes_with_call():
    field = BaseField()("field", "str")

    assert repr(field) == "BaseField('field', 'str')"
    assert str(field) == "BaseField('field', 'str')"

    assert field.default == Undefined
    assert field.default_factory == Undefined
    assert field.get_default_value() is None
    assert field.field_name == "field"
    assert field.field_type_name == "str"
    assert field.is_required() is True
    assert field.normalizers == []
    assert field.private_name == "_field"
    assert field.public_name == "field"
    assert field.validators == [validate_str]


def test_base_attributes():
    field = BaseField()

    assert repr(field) == "BaseField(default=Undefined, default_factory=Undefined, normalizers=[], validators=[])"
    assert str(field) == "BaseField(default=Undefined, default_factory=Undefined, normalizers=[], validators=[])"

    assert field.default == Undefined
    assert field.default_factory == Undefined
    assert field.get_default_value() is None
    assert field.is_required() is True
    assert field.normalizers == []
    assert field.validators == []


def test_base_set_attr():
    class Model:
        field = BaseField()("field", "str")

    model = Model()

    model.field = "value"  # set
    assert model.field == "value"  # get


def test_base_is_required():
    field = BaseField()
    assert field.is_required() is True

    field = BaseField(default=True)
    assert field.is_required() is False

    field = BaseField(default_factory=list)
    assert field.is_required() is False


def test_base_default_mutually_exclusive():
    with pytest.raises(AssertionError) as cm:
        BaseField(default=True, default_factory=list)
    assert str(cm.value) == "default and default_factory are mutually exclusive"
