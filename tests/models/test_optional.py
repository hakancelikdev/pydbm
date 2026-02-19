import typing

import pytest

from pydbm import DbmModel, Field, ValidationError


class UserModel(DbmModel):
    name: str
    nickname: typing.Optional[str]


def test_optional_field_default_none():
    user = UserModel(name="hakan")
    assert user.nickname is None


def test_optional_field_with_value():
    user = UserModel(name="hakan", nickname="hako")
    assert user.nickname == "hako"


def test_optional_field_explicit_none():
    user = UserModel(name="hakan", nickname=None)
    assert user.nickname is None


def test_optional_field_save_and_load_none(teardown_db):
    user = UserModel(name="hakan")
    user.save()

    loaded = UserModel.objects.get(id=user.id)
    assert loaded.name == "hakan"
    assert loaded.nickname is None


def test_optional_field_save_and_load_value(teardown_db):
    user = UserModel(name="hakan", nickname="hako")
    user.save()

    loaded = UserModel.objects.get(id=user.id)
    assert loaded.name == "hakan"
    assert loaded.nickname == "hako"


def test_optional_field_update_to_none(teardown_db):
    user = UserModel.objects.create(name="hakan", nickname="hako")
    assert user.nickname == "hako"

    user.update(nickname=None)
    assert user.nickname is None

    loaded = UserModel.objects.get(id=user.id)
    assert loaded.nickname is None


def test_optional_field_update_from_none(teardown_db):
    user = UserModel.objects.create(name="hakan")
    assert user.nickname is None

    user.update(nickname="hako")
    assert user.nickname == "hako"

    loaded = UserModel.objects.get(id=user.id)
    assert loaded.nickname == "hako"


def test_optional_field_validation_wrong_type():
    with pytest.raises(ValidationError) as cm:
        UserModel(name="hakan", nickname=123)

    assert cm.value.field_name == "nickname"
    assert cm.value.field_value == 123


def test_optional_field_all(teardown_db):
    UserModel.objects.create(name="hakan", nickname="hako")
    UserModel.objects.create(name="celik")

    users = sorted(list(UserModel.objects.all()), key=lambda x: x.name)
    assert users[0].name == "celik"
    assert users[0].nickname is None
    assert users[1].name == "hakan"
    assert users[1].nickname == "hako"


def test_optional_field_filter(teardown_db):
    UserModel.objects.create(name="hakan", nickname="hako")
    UserModel.objects.create(name="celik")

    result = list(UserModel.objects.filter(nickname=None))
    assert len(result) == 1
    assert result[0].name == "celik"


def test_optional_int_field(teardown_db):
    class Model(DbmModel):
        name: str
        age: typing.Optional[int]

    model = Model(name="hakan")
    assert model.age is None

    model = Model(name="hakan", age=30)
    assert model.age == 30

    model.save()
    loaded = Model.objects.get(id=model.id)
    assert loaded.age == 30


def test_optional_int_field_save_none(teardown_db):
    class Model(DbmModel):
        name: str
        age: typing.Optional[int]

    model = Model(name="hakan")
    model.save()

    loaded = Model.objects.get(id=model.id)
    assert loaded.age is None


def test_optional_field_with_custom_default():
    class Model(DbmModel):
        name: str
        nickname: typing.Optional[str] = "default_nick"

    model = Model(name="hakan")
    assert model.nickname == "default_nick"


def test_optional_field_with_field_descriptor():
    class Model(DbmModel):
        name: str
        nickname: typing.Optional[str] = Field(default="custom")

    model = Model(name="hakan")
    assert model.nickname == "custom"


def test_optional_field_repr():
    user = UserModel(name="hakan", nickname="hako")
    assert "nickname='hako'" in repr(user)

    user2 = UserModel(name="hakan")
    assert "nickname=None" in repr(user2)


def test_optional_field_eq():
    user1 = UserModel(name="hakan")
    user2 = UserModel(name="hakan")
    assert user1 == user2

    user3 = UserModel(name="hakan", nickname="hako")
    assert user1 != user3
