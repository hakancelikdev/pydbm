# Model Config

The behavior of Pydbm can be controlled via the `Config` class on a model.

```python
from pydbm import DbmModel

__all__ = (
    "UserModel",
)

class UserModel(DbmModel):
    username: str
    password: str

    class Config:
        unique_together = ("username",)
        table_name = "users"
```

In Pydbm, the default behavior of the model is to use the model's name as the `table_name`,
and the `unique_together` is set to all the fields.

## Config options

- **`table_name`** — Name of the database table (default: model name lowercased + `s`, e.g. `UserModel` → `usermodels`).
- **`unique_together`** — Tuple of field names used to generate and look up the primary key (default: all fields).
- **`abstract`** — If `True`, the model is abstract: it has no table, no `objects` manager, and cannot be instantiated. Used for [model inheritance](models.md#model-inheritance); subclasses inherit fields and can inherit this config. Default is `False`.

## Config inheritance

When a model subclasses another and does not define its own `Config`, it inherits `unique_together` from the first base that has a `Config`. The table name is always generated from the subclass name, not inherited. See [Model inheritance](models.md#model-inheritance) in the models tutorial.
