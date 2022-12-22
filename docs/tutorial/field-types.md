## Supported Types

`bool`
> Field value can be `True` or `False`.

`bytes`
> Field value can be any sequence of bytes.

`date`
> Field value can be a date object.

`datetime`
> Field value can be a datetime object.

`float`
> Field value can be a floating point number.

`int`
> Field value can be an integer.

`None`
> Field value can be `None`.

`str`
> Field value can be a string.

```python
import datetime

from pydbm import DbmModel


class User(DbmModel):
    bool_field: bool
    bytes_field: bytes
    date_field: datetime.date
    datetime_field: datetime.datetime
    float_field: float
    int_field: int
    none_field: None
    str_field: str
```

## Supported types can run after future annotations import.

```python
from __future__ import annotations

import datetime

from pydbm import DbmModel

class User(DbmModel):
    bool_field: bool
    bytes_field: bytes
    date_field: datetime.date
    datetime_field: datetime.datetime
    float_field: float
    int_field: int
    none_field: None
    str_field: str
```


## Supported types can be defined as a string form.

```python
import datetime

from pydbm import DbmModel

class User(DbmModel):
    bool_field: "bool"
    bytes_field: "bytes"
    date_field: "datetime.date"
    datetime_field: "datetime.datetime"
    float_field: "float"
    int_field: "int"
    none_field: "None"
    str_field: "str"
```
