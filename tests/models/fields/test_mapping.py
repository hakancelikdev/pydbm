from pydbm.models.fields.mapping import DictField
from pydbm.models.validators import validate_dict


def test_dict_field_check_validator():
    field = DictField()
    assert field.validators == [validate_dict]
