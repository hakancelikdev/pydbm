from datetime import date, datetime

from pydbm.models.fields.generic import GenericField

__all__ = ("DateTimeField", "DateField")


class DateTimeField(GenericField):
    def __init__(self, **kwargs) -> None:
        super().__init__(field_type=datetime, **kwargs)


class DateField(GenericField):
    def __init__(self, **kwargs) -> None:
        super().__init__(field_type=date, **kwargs)
