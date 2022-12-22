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

These can be imported from pydbm.models.validators, or just import from pydbm

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
)
```
