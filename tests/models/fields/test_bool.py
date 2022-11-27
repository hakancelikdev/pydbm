from odbm.models.fields.bool import BoolField
from odbm.models.validators import validate_bool


def test_bool_field_check_validator():
    field = BoolField()
    assert field.validators == [validate_bool]
