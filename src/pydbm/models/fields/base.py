from __future__ import annotations

import contextlib
import typing

from pydbm.exceptions import ValidationError
from pydbm.logging import logger
from pydbm.models.validators import validate_max_value, validate_min_value, validator_mapping

if typing.TYPE_CHECKING:
    from pydbm.models.base import DbmModel
    from pydbm.models.meta import Meta
    from pydbm.typing_extra import NormalizationT, SupportedClassT, ValidatorT


__all__ = (
    "BaseField",
    "Field",
    "Undefined",
)


Self = typing.TypeVar("Self", bound="BaseField")  # unexport: not-public

Undefined = type("Undefined", (), {"__repr__": lambda self: "Undefined", "__name__": "Undefined"})()


class BaseField:
    __slots__ = (
        "field_name",
        "field_type",
        "default",
        "default_factory",
        "normalizers",
        "validators",
        "public_name",
        "private_name",
        "max_value",
        "min_value",
        "kwargs",
        "_is_call_run",
    )

    def __init__(
        self,
        default: typing.Any = Undefined,
        default_factory: typing.Callable[[], typing.Any] = Undefined,
        normalizers: list[NormalizationT] | None = None,
        validators: list[ValidatorT] | None = None,
        max_value: int | None = None,
        min_value: int | None = None,
    ) -> None:  # noqa: E501
        assert not (
            default is not Undefined and default_factory is not Undefined
        ), "default and default_factory are mutually exclusive"  # noqa: E501

        self.default = default
        self.default_factory = default_factory
        self.normalizers: list[NormalizationT] = [] if normalizers is None else normalizers
        self.validators: list[ValidatorT] = [] if validators is None else validators
        self.max_value = max_value
        self.min_value = min_value

        self._is_call_run = False

    def __set_name__(self, instance: Meta, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, instance: Meta, owner: DbmModel) -> typing.Any:
        with contextlib.suppress(AttributeError):
            return getattr(instance, self.private_name)

        return self.get_default_value()

    def __set__(self, instance: DbmModel, value: typing.Any) -> None:
        if value.__class__ is int:
            if self.min_value:
                self.validators.append(validate_min_value(self.min_value))
            if self.max_value:
                self.validators.append(validate_max_value(self.max_value))
        else:
            if self.min_value or self.max_value:
                logger.warning(
                    "min_value and max_value are only valid for int type. "
                    f"They are ignored for {value.__class__.__name__} type."
                )

        normalize_and_validate_value = self.before_set(value)
        setattr(instance, self.private_name, normalize_and_validate_value)

    def __call__(self: Self, field_name: str, field_type: SupportedClassT, *args, **kwargs) -> Self:  # type: ignore[valid-type]  # noqa: E501
        self._is_call_run = True

        self.field_name = field_name
        self.field_type = field_type

        self.public_name = field_name
        self.private_name = "_" + field_name

        self.validators.append(validator_mapping[field_type])
        return self

    def __repr__(self) -> str:
        if self._is_call_run:
            return f"{self.__class__.__name__}({self.field_name!r}, {self.field_type!r})"
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
                if validator(value) is False:
                    raise ValueError("Value is not valid")
            except ValueError as exc:
                raise ValidationError(self.field_name, value, exc)

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
