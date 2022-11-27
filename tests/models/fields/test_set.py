from pydbm.models.fields.set import SetField
from pydbm.models.validators import validate_set


def test_set_field_check_validator():
    field = SetField()
    assert field.validators == [validate_set]
