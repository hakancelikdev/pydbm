### Custom Validation
We have some built-in validators, but you can also create your own validator.
For more information, see [Built-in Validators](#built-in-validators).

```python
from pydbm import DbmModel, Field

__all__ = (
    "UserModel",
)

class UserModel(DbmModel):
    username: str = Field(
        validators=[lambda value: value.startswith("@")]
    )
```


## Built-in Validators
- validate_bool
- validate_bytes
- validate_date
- validate_datetime
- validate_float
- validate_int
- validate_none
- validate_str
- validate_max_value
- validate_min_value

## Array Validators
- validate_array_int
- validate_array_float
- validate_array_str

```python
from pydbm import (
    validate_bool,
    validate_bytes,
    validate_date,
    validate_datetime,
    validate_float,
    validate_int,
    validate_none,
    validate_str,
    validate_max_value,
    validate_min_value,
    validate_array_int,
    validate_array_float,
    validate_array_str,
)
```
