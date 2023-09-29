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

`array`
> Field value can be an array of int, float and str.

This field is an alias of [`array.array`](https://docs.python.org/3/library/array.html) from the standard library.
It understands the type of the array from the type of the field, and it can be used to store arrays of int, float and str.

To use this field, firstly you need to import array from pydbm. Then you must specify the type of the array in square brackets after the type of the field.
Finally, you can use the field as a normal field.

For example, if you want to store an array of int, you can use `pydbm.array[int]` as the type of the field.
But when you want to define the type of the field, you must use `pydbm.array(...)` instead of `array[int]`.

```python
import datetime

import pydbm


class User(pydbm.DbmModel):
    bool_field: bool
    bytes_field: bytes
    date_field: datetime.date
    datetime_field: datetime.datetime
    float_field: float
    int_field: int
    none_field: None
    str_field: str
    int_array: pydbm.array[int]
    float_array: pydbm.array[float]
    str_array: pydbm.array[str]
```
