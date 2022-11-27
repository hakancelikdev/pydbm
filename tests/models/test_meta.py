import pytest

from pydbm import exceptions
from pydbm.models import meta
from pydbm.models.fields import AutoField


class BaseModel(metaclass=meta.Meta):
    def __init__(self, **kwargs):
        kwargs.pop("pk")
        for name, value in kwargs.items():
            setattr(self, name, value)


def test_generate_table_name():
    assert meta.generate_table_name("User") == "users"
    assert meta.generate_table_name("UserModel") == "usermodels"


def test_config():
    config = meta.Config(table_name="users", unique_together=("email", "username"))

    assert config.table_name == "users"
    assert config.unique_together == ("email", "username")


def test_get_config():
    config = meta.get_config("User", None)

    assert config.table_name == "users"
    assert config.unique_together == ()

    config = meta.get_config("User", meta.Config(table_name="users", unique_together=("email", "username")))

    assert config.table_name == "users"
    assert config.unique_together == ("email", "username")


def test_meta():
    class User(BaseModel):
        email: str
        username: str

    user = User(email="hakancelikdev@gmail.com", username="hakancelikdev")

    assert user.email == "hakancelikdev@gmail.com"
    assert user.username == "hakancelikdev"
    assert user.pk == "7caae990504a6f4c4c8f436a3d8d009f"
    assert user.required_fields == ["email", "username"]
    assert isinstance(user.not_required_fields[0], AutoField)
    assert user.not_required_fields[0].public_name == "pk"
    assert user.database.table_name == "users"
    assert user.__dict__ == {}
    assert user.__slots__ == ("_email", "_pk", "_username")


def test_meta_config():
    class User(BaseModel):
        email: str
        username: str

        class Config:
            table_name = "user_table"
            unique_together = ("email", "username")

    user = User(email="hakancelikdev@gmail.com", username="hakancelikdev")
    assert user.pk == "7caae990504a6f4c4c8f436a3d8d009f"
    assert isinstance(user.not_required_fields[0], AutoField)
    assert user.not_required_fields[0].public_name == "pk"
    assert user.database.table_name == "user_table"


def test_meta_is_required_error():
    class Example(BaseModel):
        field: str

    with pytest.raises(ValueError) as cm:
        assert Example()

    assert cm.value.args[0] == "field is required"


def test_base_type_validator():
    class Model(BaseModel):
        str: str
        int: int
        float: float
        tuple: tuple
        list: list
        dict: dict
        set: set
        bool: bool
        bytes: bytes

    with pytest.raises(exceptions.OdbmValidationError) as cm:
        Model(str=1, int=1, float=1.0, tuple=(1, 2), list=[1, 2], dict={"a": 1}, set={1, 2}, bool=True, bytes=b"123")
    assert str(cm.value) == "Invalid value for str=1; It must be str, not int"

    with pytest.raises(exceptions.OdbmValidationError) as cm:
        Model(
            str="str", int=1.1, float=1.0, tuple=(1, 2), list=[1, 2], dict={"a": 1}, set={1, 2}, bool=True, bytes=b"123"
        )
    assert str(cm.value) == "Invalid value for int=1.1; It must be int, not float"

    with pytest.raises(exceptions.OdbmValidationError) as cm:
        Model(
            str="str",
            int=1,
            float=(1.0,),
            tuple=(1, 2),
            list=[1, 2],
            dict={"a": 1},
            set={1, 2},
            bool=True,
            bytes=b"123",
        )
    assert str(cm.value) == "Invalid value for float=(1.0,); It must be float, not tuple"

    with pytest.raises(exceptions.OdbmValidationError) as cm:
        Model(
            str="str", int=1, float=1.0, tuple=[1, 2], list=[1, 2], dict={"a": 1}, set={1, 2}, bool=True, bytes=b"123"
        )
    assert str(cm.value) == "Invalid value for tuple=[1, 2]; It must be tuple, not list"

    with pytest.raises(exceptions.OdbmValidationError) as cm:
        Model(
            str="str", int=1, float=1.0, tuple=(1, 2), list=(1, 2), dict={"a": 1}, set={1, 2}, bool=True, bytes=b"123"
        )
    assert str(cm.value) == "Invalid value for list=(1, 2); It must be list, not tuple"

    # with pytest.raises(exceptions.OdbmValidationError) as cm:  # TODO: fix it
    #     Model(
    #         str="str", int=1, float=1.0, tuple=(1, 2), list=[1, 2], dict={"a", 1}, set={1, 2}, bool=True, bytes=b"123"
    #     )
    # assert str(cm.value) == "Invalid value for dict={1, 'a'}; It must be dict, not set"

    with pytest.raises(exceptions.OdbmValidationError) as cm:
        Model(
            str="str", int=1, float=1.0, tuple=(1, 2), list=[1, 2], dict={"a": 1}, set={"1": 2}, bool=True, bytes=b"123"
        )
    assert str(cm.value) == "Invalid value for set={'1': 2}; It must be set, not dict"

    with pytest.raises(exceptions.OdbmValidationError) as cm:
        Model(str="str", int=1, float=1.0, tuple=(1, 2), list=[1, 2], dict={"a": 1}, set={1, 2}, bool=1, bytes=b"123")
    assert str(cm.value) == "Invalid value for bool=1; It must be bool, not int"

    with pytest.raises(exceptions.OdbmValidationError) as cm:
        Model(str="str", int=1, float=1.0, tuple=(1, 2), list=[1, 2], dict={"a": 1}, set={1, 2}, bool=True, bytes="123")
    assert str(cm.value) == "Invalid value for bytes='123'; It must be bytes, not str"
