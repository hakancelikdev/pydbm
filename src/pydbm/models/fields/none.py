from pydbm.models.fields.base import BaseField
from pydbm.models.validators import validate_none

__all__ = ("NoneField",)


class NoneField(BaseField):
    def __init__(self, **kwargs) -> None:
        validators = kwargs.pop("validators", [])
        validators.append(validate_none)
        super().__init__(validators=validators, **kwargs)
