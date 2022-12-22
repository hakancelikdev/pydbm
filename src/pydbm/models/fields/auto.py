from __future__ import annotations

import hashlib
import typing

from pydbm.models.fields.base import BaseField

if typing.TYPE_CHECKING:
    from pydbm.models.base import DbmModel
    from pydbm.models.meta import Meta
    from pydbm.typing_extra import SupportedClassT

__all__ = (
    "AutoField",
)

Self = typing.TypeVar("Self", bound="AutoField")  # unexport: not-public


class AutoField(BaseField):
    __slots__ = (
        "unique_together",
        "fields",
    )

    def __init__(self, field_name: str, field_type: SupportedClassT, *, unique_together: tuple[str, ...] | None = None, **kwargs) -> None:  # noqa: E501
        self.field_name = field_name
        self.field_type = field_type

        self.public_name = field_name
        self.private_name = "_" + field_name

        self.unique_together = unique_together if unique_together is not None else ()
        super().__init__(default_factory=self.generate_pk, **kwargs)

    def __get__(self, instance: Meta, owner: DbmModel) -> typing.Any:
        return self.get_default_value()

    def __set__(self, instance: DbmModel, value: typing.Any) -> None:
        raise AttributeError("AutoField is read-only")

    def __call__(self: Self, fields: dict[str, typing.Any] | None = None, *args, **kwargs) -> Self:  # type: ignore[valid-type, override]  # noqa: E501
        if self.unique_together and not fields:
            raise ValueError("unique_together ise set, fields must be passed")

        self.fields = fields
        return super().__call__(self.field_name, self.field_type, *args, **kwargs)  # type: ignore

    def generate_pk(self) -> str:
        if self.unique_together and self._is_call_run:
            text = "*".join(map(str, (attr for name in self.unique_together if (attr := self.fields.get(name, None)))))
            return hashlib.md5(bytes(text, "utf-8")).hexdigest()
        else:
            return __import__("uuid").uuid4().hex
