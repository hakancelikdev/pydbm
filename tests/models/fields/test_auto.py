import pytest

from pydbm.models.fields.auto import AutoField


def test_auto_field_repr():
    field = AutoField("pk", "str")
    assert repr(field) == "AutoField(default=Undefined, default_factory=generate_pk, normalizers=[], validators=[])"
    assert repr(field()) == "AutoField('pk', 'str')"


def test_auto_field():
    class Model:
        pk = AutoField("pk", "str")()

    model = Model()
    assert model.pk

    with pytest.raises(AttributeError) as cm:
        model.pk = "str"
    assert str(cm.value) == "AutoField is read-only"

    class Model:
        pk = AutoField("pk", "str", unique_together=("name", "username"))({"name": "hakan", "username": "hakancelik"})

    model = Model()
    assert model.pk == "e2cd7febd091a509284e8ab0fc302fbb"
