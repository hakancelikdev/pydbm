import typing

from pydbm.models.fields.base import BaseField

__all__ = ("GenericField",)


class GenericField(BaseField):
    def __init__(self, *, field_type: typing.Type, **kwargs) -> None:
        validators = kwargs.pop("validators", [])
        validators.append(self.validator(field_type))

        super().__init__(validators=validators, **kwargs)

    @staticmethod
    def validator(field_type) -> typing.Callable[[typing.Any], None]:
        from pydbm.models import validators

        return getattr(validators, f"validate_{field_type.__name__.lower()}")
