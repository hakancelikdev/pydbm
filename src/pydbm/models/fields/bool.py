from pydbm.models.fields.generic import GenericField

__all__ = ("BoolField",)


class BoolField(GenericField):
    def __init__(self, **kwargs) -> None:
        super().__init__(field_type=bool, **kwargs)
