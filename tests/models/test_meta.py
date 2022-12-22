import datetime

import pytest

from pydbm import exceptions
from pydbm.models import meta
from pydbm.models.fields import AutoField


class DbmModel(metaclass=meta.Meta):
    def __init__(self, **kwargs):
        kwargs.pop("pk")
        for name, value in kwargs.items():
            setattr(self, name, value)


def test_generate_table_name():
    assert meta.Meta.generate_table_name("User") == "users"
    assert meta.Meta.generate_table_name("UserModel") == "usermodels"


def test_config():
    config = meta.Config(table_name="users", unique_together=("email", "username"))

    assert config.table_name == "users"
    assert config.unique_together == ("email", "username")


def test_get_config():
    config = meta.Meta.get_config("User", {})

    assert config.table_name == "users"
    assert config.unique_together == ()

    config = meta.Meta.get_config(
        "User", {meta.CLASS_CONFIG_NAME: meta.Config(table_name="users", unique_together=("email", "username"))}
    )

    assert config.table_name == "users"
    assert config.unique_together == ("email", "username")


def test_meta():
    class User(DbmModel):
        email: str
        username: str

    user = User(email="hakancelikdev@gmail.com", username="hakancelikdev")

    assert user.email == "hakancelikdev@gmail.com"
    assert user.username == "hakancelikdev"
    assert user.pk == "7caae990504a6f4c4c8f436a3d8d009f"
    assert user.required_fields == ["email", "username"]
    assert isinstance(user.not_required_fields[0], AutoField)
    assert user.not_required_fields[0].public_name == "pk"
    assert user.objects.table_name == "users"
    assert not hasattr(user, "__dict__")
    assert user.__slots__ == ("_email", "_pk", "_username", "database")


def test_meta_config():
    class User(DbmModel):
        email: str
        username: str

        class Config:
            table_name = "user_table"
            unique_together = ("email", "username")

    user = User(email="hakancelikdev@gmail.com", username="hakancelikdev")
    assert user.pk == "7caae990504a6f4c4c8f436a3d8d009f"
    assert isinstance(user.not_required_fields[0], AutoField)
    assert user.not_required_fields[0].public_name == "pk"
    assert user.objects.table_name == "user_table"


def test_meta_is_required_error():
    class Example(DbmModel):
        field: str

    with pytest.raises(ValueError) as cm:
        assert Example()

    assert cm.value.args[0] == "field is required"


@pytest.mark.parametrize(
    "updated_fields, expected_error_ms",
    [
        ({"bool": 1}, "Invalid value for bool=1; It must be bool."),
        ({"bytes": "123"}, "Invalid value for bytes='123'; It must be bytes."),
        ({"date": datetime.datetime(2020, 1, 1)}, "Invalid value for date=datetime.datetime(2020, 1, 1, 0, 0); It must be date."),  # noqa: E501
        ({"datetime": datetime.date(2020, 1, 1)}, "Invalid value for datetime=datetime.date(2020, 1, 1); It must be datetime."),  # noqa: E501
        ({"float": (1.0,)}, "Invalid value for float=(1.0,); It must be float."),
        ({"int": 1.1}, "Invalid value for int=1.1; It must be int."),
        ({"none": b"test"}, "Invalid value for none=b'test'; It must be None."),
        ({"str": 1}, "Invalid value for str=1; It must be str."),
    ],
)
def test_base_type_validator(updated_fields, expected_error_ms):
    class Model(DbmModel):
        bool: bool
        bytes: bytes
        date: datetime.date
        datetime: datetime.datetime
        float: float
        int: int
        none: None
        str: str

    model_body = {
        "bool": True,
        "bytes": b"123",
        "date": datetime.date.today(),
        "datetime": datetime.datetime.now(),
        "float": 1.0,
        "int": 1,
        "none": None,
        "str": "str",
    }
    model_body.update(updated_fields)

    with pytest.raises(exceptions.ValidationError) as cm:
        Model(**model_body)
    assert str(cm.value) == expected_error_ms
