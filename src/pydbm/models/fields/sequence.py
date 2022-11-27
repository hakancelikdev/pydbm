from pydbm.models.fields import GenericField
from pydbm.models.validators import validate_max_value, validate_min_value

__all__ = ("ListField", "TupleField", "BytesField", "StrField")


class StrField(GenericField):
    def __init__(self, max_value: int | None = None, min_value: int | None = None, **kwargs) -> None:
        validators = kwargs.pop("validators", [])

        if max_value is not None:
            validators.append(validate_max_value(max_value))

        if min_value is not None:
            validators.append(validate_min_value(min_value))
        super().__init__(field_type=str, validators=validators, **kwargs)


class BytesField(GenericField):
    def __init__(self, **kwargs) -> None:
        super().__init__(field_type=bytes, **kwargs)


class ListField(GenericField):
    def __init__(self, max_value: int | None = None, min_value: int | None = None, **kwargs) -> None:
        validators = kwargs.pop("validators", [])

        if max_value is not None:
            validators.append(validate_max_value(max_value))

        if min_value is not None:
            validators.append(validate_min_value(min_value))
        super().__init__(field_type=list, validators=validators, **kwargs)


class TupleField(GenericField):
    def __init__(self, max_value: int | None = None, min_value: int | None = None, **kwargs) -> None:
        validators = kwargs.pop("validators", [])

        if max_value is not None:
            validators.append(validate_max_value(max_value))

        if min_value is not None:
            validators.append(validate_min_value(min_value))
        super().__init__(field_type=tuple, validators=validators, **kwargs)
