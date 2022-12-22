from __future__ import annotations

import abc
import typing

if typing.TYPE_CHECKING:
    from pydbm.typing_extra import SupportedClassT

__all__ = (
    "BaseDataType",
)


class BaseDataType(abc.ABC):
    data_types: dict[SupportedClassT, typing.Type[BaseDataType]] = {}

    @staticmethod
    @abc.abstractmethod
    def get(value: str) -> typing.Any:
        pass

    @staticmethod
    @abc.abstractmethod
    def set(value: typing.Any) -> str:
        pass

    def __init_subclass__(cls, data_type: SupportedClassT, **kwargs):  # noqa
        super().__init_subclass__(**kwargs)
        cls.data_types[data_type] = cls

    @classmethod
    def get_data_type(cls, item: SupportedClassT) -> typing.Type[BaseDataType]:
        try:
            return cls.data_types[item]
        except KeyError:
            raise TypeError(f"Type {item} is not supported yet!")
