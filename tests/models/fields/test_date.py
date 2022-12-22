from datetime import date, datetime

import pytest

from pydbm import DbmModel, Field, ValidationError


@pytest.mark.parametrize(
    "value",
    [
        datetime(2020, 1, 1),
    ],
)
def test_valid_datetime_field(value):
    class Model(DbmModel):
        field: datetime = Field()

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
        date(2020, 1, 1),
        b"byte",
        1.1,
        -1.1,
    ],
)
def test_invalid_datetime_field(value):
    class Model(DbmModel):
        field: datetime = Field()

    with pytest.raises(ValidationError) as cm:
        Model(field=value)

    assert cm.value.error.args[0] == "It must be datetime"
    assert cm.value.field_name == "field"
    assert cm.value.field_value == value


@pytest.mark.parametrize(
    "value",
    [
        date(2020, 1, 1),
    ],
)
def test_valid_date_field(value):
    class Model(DbmModel):
        field: date = Field()

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
        b"byte",
        1.1,
        -1.1,
    ],
)
def test_invalid_date_field(value):
    class Model(DbmModel):
        field: date = Field()

    with pytest.raises(ValidationError) as cm:
        Model(field=value)

    assert cm.value.error.args[0] == "It must be date"
    assert cm.value.field_name == "field"
    assert cm.value.field_value == value
