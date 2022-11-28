from datetime import date, datetime

import pytest

from pydbm import BaseModel, Field, ValidationError


@pytest.mark.parametrize(
    "value",
    [
        {},
        {"a": 1},
        {"a": 1, "b": 2},
        {"a": 1, "b": 2, "c": 3},
        {"a": 1, "b": 2, "c": 3, "d": 4},
        {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5},
    ],
)
def test_valid_dict_field(value):
    class Model(BaseModel):
        field: dict = Field()

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
def test_invalid_dict_field(value):
    class Model(BaseModel):
        field: dict = Field()

    with pytest.raises(ValidationError) as cm:
        Model(field=value)

    assert cm.value.error.args[0] == "It must be dict"
    assert cm.value.field_name == "field"
    assert cm.value.field_value == value
