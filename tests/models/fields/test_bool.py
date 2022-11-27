from pydbm.models.fields.bool import BoolField
from pydbm.models.validators import validate_bool


def test_bool_field_check_validator():
    field = BoolField()
    assert field.validators == [validate_bool]
