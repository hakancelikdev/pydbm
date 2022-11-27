from __future__ import annotations

import contextlib
import typing

from pydbm.exceptions import OdbmValidationError
from pydbm.models import validators as odbm_validators

if typing.TYPE_CHECKING:
    from pydbm.models.base import BaseModel
    from pydbm.models.meta import Meta


__all__ = ("AnyCallableFunctionT", "BaseField", "Undefined", "Field")


Undefined = type("Undefined", (), {"__repr__": lambda self: "Undefined", "__name__": "Undefined"})()
AnyCallableFunctionT = typing.List[typing.Callable[[typing.Any], typing.Any]]
Self = typing.TypeVar("Self", bound="BaseField")  # unexport: not-public


class BaseField:
    __slots__ = (
        "field_name",
        "field_type_name",
        "default",
        "default_factory",
        "normalizers",
        "validators",
        "public_name",
        "private_name",
        "field_name",
        "field_type_name",
        "__is_call_run",
    )

    def __init__(
        self,
        default: typing.Any = Undefined,
        default_factory: typing.Callable[[], typing.Any] = Undefined,
        normalizers: AnyCallableFunctionT | None = None,
        validators: AnyCallableFunctionT | None = None,
        **kwargs,
    ) -> None:  # noqa: E501
        assert not (
            default is not Undefined and default_factory is not Undefined
        ), "default and default_factory are mutually exclusive"  # noqa: E501

        self.default = default
        self.default_factory = default_factory
        self.normalizers: AnyCallableFunctionT = [] if normalizers is None else normalizers
        self.validators: AnyCallableFunctionT = [] if validators is None else validators

        self.__is_call_run = False

    def __set_name__(self, instance: Meta, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, instance: Meta, owner: BaseModel) -> typing.Any:
        with contextlib.suppress(AttributeError):
            return getattr(instance, self.private_name)

        return self.get_default_value()

    def __set__(self, instance: BaseModel, value: typing.Any) -> None:
        normalize_and_validate_value = self.before_set(value)

        setattr(instance, self.private_name, normalize_and_validate_value)

    def __call__(self: Self, field_name: str, field_type_name: str, *args, **kwargs) -> Self:  # type: ignore[valid-type]  # noqa: E501
        self.__is_call_run = True

        self.field_name = field_name
        self.field_type_name = field_type_name

        self.public_name = field_name
        self.private_name = "_" + field_name

        self.validators.append(getattr(odbm_validators, f"validate_{self.field_type_name}"))
        return self

    def __repr__(self) -> str:
        if self.__is_call_run:
            return f"{self.__class__.__name__}({self.field_name!r}, {self.field_type_name!r})"
        return (
            f"{self.__class__.__name__}("
            f"default={self.default!r}, "
            f"default_factory={self.default_factory.__name__}, "
            f"normalizers={self.normalizers!r}, "
            f"validators={self.validators!r}"
            f")"
        )

    def before_set(self, value: typing.Any) -> typing.Any:
        for normalizer in self.normalizers:
            value = normalizer(value)

        for validator in self.validators:
            try:
                validator(value)
            except ValueError as exc:
                raise OdbmValidationError(self.field_name, value, exc)

        return value

    def is_required(self) -> bool:
        return self.default is Undefined and self.default_factory is Undefined

    def get_default_value(self) -> typing.Any:
        if self.default is not Undefined:
            return self.default

        if self.default_factory is not Undefined:
            return self.default_factory()


class Field(BaseField):
    pass
