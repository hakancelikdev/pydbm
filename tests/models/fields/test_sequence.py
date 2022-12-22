from datetime import date, datetime

import pytest

from pydbm import DbmModel, Field, ValidationError


@pytest.mark.parametrize(
    "value",
    [
        "",
        "True",
        "False",
        "[]",
        "{}",
        "set()",
        "tuple()",
        "object()",
        "datetime(2020, 1, 1)",
        "date(2020, 1, 1)",
    ],
)
def test_valid_str_field(value):
    class Model(DbmModel):
        field: str = Field()

    model = Model(field=value)
    assert model.field == value


def test_str_default():
    class Model(DbmModel):
        field: str = Field(default="10")

    model = Model()
    assert model.field == "10"


def test_str_default_factory():
    class Model(DbmModel):
        field: str = Field(default_factory=lambda: "10")

    model = Model()
    assert model.field == "10"


def test_str_default_factory_and_default():
    with pytest.raises(AssertionError) as cm:

        class Model(DbmModel):
            field: str = Field(default_factory=lambda: "10", default="20")

    assert str(cm.value) == "default and default_factory are mutually exclusive"


def test_str_max_value(caplog):
    class Model(DbmModel):
        field: str = Field(max_value=10)

    caplog.clear()
    with caplog.at_level("WARNING"):
        Model(field="11")
    assert (
        caplog.records[0].msg == "min_value and max_value are only valid for int type. They are ignored for str type."
    )


def test_str_min_value(caplog):
    class Model(DbmModel):
        field: str = Field(min_value="10")

    caplog.clear()
    with caplog.at_level("WARNING"):
        Model(field="2")
    assert (
        caplog.records[0].msg == "min_value and max_value are only valid for int type. They are ignored for str type."
    )


@pytest.mark.parametrize(
    "value",
    [
        -1,
        None,
        0,
        1,
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
def test_invalid_str_field(value):
    class Model(DbmModel):
        field: str = Field()

    with pytest.raises(ValidationError) as cm:
        Model(field=value)

    assert cm.value.error.args[0] == "It must be str"
    assert cm.value.field_name == "field"
    assert cm.value.field_value == value


@pytest.mark.parametrize(
    "value",
    [
        b"",
        b"True",
        b"False",
        b"[]",
        b"{}",
        b"set()",
        b"tuple()",
        b"object()",
        b"datetime(2020, 1, 1)",
        b"date(2020, 1, 1)",
    ],
)
def test_valid_bytes_field(value):
    class Model(DbmModel):
        field: bytes = Field()

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
        1.1,
        -1.1,
    ],
)
def test_invalid_bytes_field(value):
    class Model(DbmModel):
        field: bytes = Field()

    with pytest.raises(ValidationError) as cm:
        Model(field=value)

    assert cm.value.error.args[0] == "It must be bytes"
    assert cm.value.field_name == "field"
    assert cm.value.field_value == value
