from datetime import date, datetime

import pytest

from pydbm import DbmModel, Field, ValidationError


@pytest.mark.parametrize(
    "value",
    [
        -1,
        0,
        1,
    ],
)
def test_valid_int_field(value):
    class Model(DbmModel):
        field: int = Field()

    model = Model(field=value)
    assert model.field == value


def test_int_default():
    class Model(DbmModel):
        field: int = Field(default=10)

    model = Model()
    assert model.field == 10


def test_int_default_factory():
    class Model(DbmModel):
        field: int = Field(default_factory=lambda: 10)

    model = Model()
    assert model.field == 10


def test_int_max_value():
    class Model(DbmModel):
        field: int = Field(max_value=10)

    with pytest.raises(ValidationError) as cm:
        Model(field=11)
    assert str(cm.value) == "Invalid value for field=11; It must be less than 10."


def test_int_min_value():
    class Model(DbmModel):
        field: int = Field(min_value=10)

    with pytest.raises(ValidationError) as cm:
        Model(field=9)
    assert str(cm.value) == "Invalid value for field=9; It must be greater than 10."


def test_int_min_and_max_value():
    class Model(DbmModel):
        field: int = Field(min_value=10, max_value=20)

    with pytest.raises(ValidationError) as cm:
        Model(field=9)
    assert str(cm.value) == "Invalid value for field=9; It must be greater than 10."

    with pytest.raises(ValidationError) as cm:
        Model(field=21)
    assert str(cm.value) == "Invalid value for field=21; It must be less than 20."


@pytest.mark.parametrize(
    "value",
    [
        None,
        "",
        "True",
        "False",
        [],
        {},
        set(),
        tuple(),
        object(),
        datetime(2020, 1, 1),
        date(2020, 1, 1),
        b"byte",
        1.1,
        -1.1,
    ],
)
def test_invalid_int_field(value):
    class Model(DbmModel):
        field: int = Field()

    with pytest.raises(ValidationError) as cm:
        Model(field=value)

    assert cm.value.error.args[0] == "It must be int"
    assert cm.value.field_name == "field"
    assert cm.value.field_value == value


@pytest.mark.parametrize(
    "value",
    [
        -0.1,
        0.1,
    ],
)
def test_valid_float_field(value):
    class Model(DbmModel):
        field: float = Field()

    model = Model(field=value)
    assert model.field == value


@pytest.mark.parametrize(
    "value",
    [
        -1,
        None,
        0,
        1,
        "",
        "True",
        "False",
        [],
        {},
        set(),
        tuple(),
        object(),
        datetime(2020, 1, 1),
        date(2020, 1, 1),
        b"byte",
    ],
)
def test_invalid_float_field(value):
    class Model(DbmModel):
        field: float = Field()

    with pytest.raises(ValidationError) as cm:
        Model(field=value)

    assert cm.value.error.args[0] == "It must be float"
    assert cm.value.field_name == "field"
    assert cm.value.field_value == value
