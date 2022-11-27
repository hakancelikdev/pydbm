from pydbm.models.fields.generic import GenericField

__all__ = ("SetField",)


class SetField(GenericField):
    def __init__(self, **kwargs) -> None:
        super().__init__(field_type=set, **kwargs)
