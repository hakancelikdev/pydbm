The behavior of Pydbm can be controlled via the Config class on a model.

```python
from pydbm import BaseModel

__all__ = ["UserModel"]

class UserModel(BaseModel):
    username: str
    password: str

    class Config:
        unique_together = ("username",)
        table_name = "users"
```

In Pydbm, the default behavior of the model is to use the model's name as the `table_name`.
and the `unique_together` is set to all the fields.

