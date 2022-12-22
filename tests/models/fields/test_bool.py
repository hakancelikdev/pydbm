from datetime import date, datetime

import pytest

from pydbm import DbmModel, Field, ValidationError


@pytest.mark.parametrize("value", [True, False])
def test_valid_bool_field(value):
    class Model(DbmModel):
        field: bool = Field()

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
        1.1,
        -1.1,
    ],
)
def test_invalid_bool_field(value):
    class Model(DbmModel):
        field: bool = Field()

    with pytest.raises(ValidationError) as cm:
        Model(field=value)

    assert cm.value.error.args[0] == "It must be bool"
    assert cm.value.field_name == "field"
    assert cm.value.field_value == value
