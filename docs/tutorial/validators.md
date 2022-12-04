### Custom Validation
We have some built-in validators, but you can also create your own validator.
For more information, see [Built-in Validators](#built-in-validators).

```python
from pydbm import BaseModel, Field

__all__ = ["UserModel"]

class UserModel(BaseModel):
    username: str = Field(
        validators=[lambda value: value.startswith("@")]
    )
```


## Built-in Validators
- validate_bool
- validate_bytes
- validate_date
- validate_datetime
- validate_dict
- validate_float
- validate_int
- validate_list
- validate_none
- validate_set
- validate_str
- validate_tuple
- validate_max_value
- validate_min_value

These can be imported from pydbm.models.validators, or just import from pydbm

```python
from pydbm import (
    validate_bool,
    validate_bytes,
    validate_date,
    validate_datetime,
    validate_dict,
    validate_float,
    validate_int,
    validate_list,
    validate_none,
    validate_set,
    validate_str,
    validate_tuple,
    validate_max_value,
    validate_min_value,
)
```
