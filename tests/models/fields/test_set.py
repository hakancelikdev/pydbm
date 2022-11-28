from datetime import date, datetime

import pytest

from pydbm import BaseModel, Field, ValidationError


@pytest.mark.parametrize(
    "value",
    [
        {1, 2},
        {1, 2, 3},
        {"a", "b"},
        {"a", "b", "c"},
        set(),
    ],
)
def test_valid_set_field(value):
    class Model(BaseModel):
        field: set = Field()

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
        tuple(),
        object(),
        datetime(2020, 1, 1),
        date(2020, 1, 1),
        b"byte",
        1.1,
        -1.1,
    ],
)
def test_invalid_set_field(value):
    class Model(BaseModel):
        field: set = Field()

    with pytest.raises(ValidationError) as cm:
        Model(field=value)

    assert cm.value.error.args[0] == "It must be set"
    assert cm.value.field_name == "field"
    assert cm.value.field_value == value
