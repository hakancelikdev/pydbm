from pydbm.models.fields import GenericField

__all__ = ("DictField",)


class DictField(GenericField):
    def __init__(self, **kwargs) -> None:
        super().__init__(field_type=dict, **kwargs)
