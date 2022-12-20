from __future__ import annotations

import abc
import typing

__all__ = ("BaseDataType",)


class BaseDataType(abc.ABC):
    data_types: dict[str, typing.Type[BaseDataType]] = {}

    @staticmethod
    @abc.abstractmethod
    def get(value: str) -> typing.Any:
        pass

    @staticmethod
    @abc.abstractmethod
    def set(value: typing.Any) -> str:
        pass

    def __init_subclass__(cls, data_type: typing.Type[typing.Any] | None = None, **kwargs):
        super().__init_subclass__(**kwargs)

        if data_type is not None:
            cls.data_types[data_type.__name__] = cls

    @classmethod
    def get_data_type(cls, item: str) -> typing.Type[BaseDataType]:
        try:
            return cls.data_types[item]
        except KeyError:
            raise TypeError(f"Type {item} is not supported yet!")
