## Supported Types

`bool`
> Field value can be `True` or `False`.

`bytes`
> Field value can be any sequence of bytes.

`date`
> Field value can be a date object.

`datetime`
> Field value can be a datetime object.

`dict`
> Field value can be a dictionary. Consider using an [Embed Model](embed-models.md) instead for better type safety.

`float`
> Field value can be a floating point number.

`int`
> Field value can be an integer.

`None`
> Field value can be `None`.

`str`
> Field value can be a string.

`DbmModel` (Embed Model)
> Field value can be an instance of another DbmModel subclass. See [Embed Models](embed-models.md) for details.

## Optional Types

Any supported type can be made optional using `Optional[T]` or `T | None` (Python 3.10+).
Optional fields default to `None` if no value is provided and accept both the inner type value and `None`.

```python
import typing

from pydbm import DbmModel


class User(DbmModel):
    name: str
    nickname: typing.Optional[str]  # defaults to None, accepts str or None
    age: typing.Optional[int]       # defaults to None, accepts int or None
```

```python
user = User(name="hakan")
assert user.nickname is None
assert user.age is None

user = User(name="hakan", nickname="hako", age=30)
assert user.nickname == "hako"
assert user.age == 30
```

You can also provide a custom default value for optional fields:

```python
class User(DbmModel):
    name: str
    nickname: typing.Optional[str] = "anonymous"

user = User(name="hakan")
assert user.nickname == "anonymous"
```

## Example

```python
import datetime

from pydbm import DbmModel


class User(DbmModel):
    bool_field: bool
    bytes_field: bytes
    date_field: datetime.date
    datetime_field: datetime.datetime
    dict_field: dict
    float_field: float
    int_field: int
    none_field: None
    str_field: str
```
