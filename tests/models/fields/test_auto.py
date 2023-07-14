
from pydbm.models.fields import AutoField


def test_auto_field_repr():
    field = AutoField("id", str)
    assert repr(field) == "AutoField(default=Undefined, default_factory=generate_id, normalizers=[], validators=[])"
    assert repr(field()) == f"AutoField('id', {str!r})"


def test_auto_field():
    class Model:
        id = AutoField("id", str)()

    model = Model()
    assert model.id

    model.id = "str"
    assert model.id != "str"

    class Model:
        id = AutoField("id", str, unique_together=("name", "username"))({"name": "hakan", "username": "hakancelik"})

    model = Model()
    assert model.id == "e2cd7febd091a509284e8ab0fc302fbb"
