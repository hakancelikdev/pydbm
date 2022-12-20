## Supported Types

`bool`
> Field value can be `True` or `False`.

`bytes`
> Field value can be any sequence of bytes.

[//]: # (`dict`)

[//]: # (> Field value can be a dictionary.)

[//]: # (>> But for now, Pydbm can not validators dict of type.)

[//]: # (> Only validate type of the field is dict.)

`date`
> Field value can be a date object.

`datetime`
> Field value can be a datetime object.

`float`
> Field value can be a floating point number.

[//]: # (`list`)

[//]: # (> Field value can be a list.)

[//]: # (>> But for now, Pydbm can not validators list of type.)

[//]: # (> Only validate type of the field is list.)

[//]: # (`set`)

[//]: # (> Field value can be a set.)

[//]: # (>> But for now, Pydbm can not validators set of type.)

[//]: # (> Only validate type of the field is set.)

`int`
> Field value can be an integer.

`None`
> Field value can be `None`.

`str`
> Field value can be a string.

[//]: # (`tuple`)

[//]: # (> Field value can be a tuple.)

[//]: # (>> But for now, Pydbm can not validators tuple of type.)

[//]: # (> Only validate type of the field is tuple.)

---

```python
import datetime

from pydbm import BaseModel


class User(BaseModel):
    bool_field: bool
    bytes_field: bytes
    date_field: datetime.date
    datetime_field: datetime.datetime
    float_field: float
    int_field: int
    none_field: None
    str_field: str


user = User(
    bool_field=True,
    bytes_field=b'bytes',
    date_field=datetime.date(2020, 1, 1),
    datetime_field=datetime.datetime(2020, 1, 1, 0, 0, 0),
    float_field=1.0,
    int_field=1,
    none_field=None,
    str_field='str',
)

user.save()
```
