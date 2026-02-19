## Normalizers

Normalizers are functions that transform field values before validation.
They run in order, and each normalizer receives the output of the previous one.
This is useful for cleaning, formatting, or transforming data before it is validated and stored.

### How It Works

When a value is set on a field, the processing order is:

1. **Normalizers** run first - transform the value
2. **Validators** run second - validate the transformed value

### Basic Usage

Pass a list of normalizer functions to the `normalizers` parameter of `Field`:

```python
from pydbm import DbmModel, Field


class UserModel(DbmModel):
    username: str = Field(normalizers=[lambda x: x.lower()])
```

```python
user = UserModel(username="HakanCelik")
assert user.username == "hakancelik"
```

### Chaining Multiple Normalizers

You can chain multiple normalizers. They run in order:

```python
from pydbm import DbmModel, Field


class UserModel(DbmModel):
    username: str = Field(normalizers=[str.strip, str.lower])
```

```python
user = UserModel(username="  HakanCelik  ")
assert user.username == "hakancelik"
```

### Using Named Functions

For more complex transformations, define named functions:

```python
from pydbm import DbmModel, Field


def remove_special_chars(value: str) -> str:
    return "".join(c for c in value if c.isalnum())


def truncate(value: str) -> str:
    return value[:20]


class UserModel(DbmModel):
    username: str = Field(
        normalizers=[str.strip, str.lower, remove_special_chars, truncate]
    )
```

### Normalizer Signature

A normalizer is any callable that takes a value and returns the transformed value:

```python
def normalizer(value: Any) -> Any:
    ...
```

The type is defined as `NormalizationT = Callable[[Any], Any]` and can be imported from pydbm:

```python
from pydbm import NormalizationT
```

### Normalizers with Validators

Normalizers run before validators, so validators see the already-transformed value:

```python
from pydbm import DbmModel, Field


def min_length(value: str) -> None:
    if len(value) < 3:
        raise ValueError("Username must be at least 3 characters")


class UserModel(DbmModel):
    username: str = Field(
        normalizers=[str.strip, str.lower],
        validators=[min_length],
    )
```

In this example, the username is first stripped and lowered, then validated for minimum length.
