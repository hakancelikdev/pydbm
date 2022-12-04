## Supported Types

`bool`
> Field value can be `True` or `False`.

`bytes`
> Field value can be any sequence of bytes.

`date`
> Field value can be a date in the format `YYYY-MM-DD`.

`datetime`
> Field value can be a date and time in the format `YYYY-MM-DD HH:MM:SS`.

`dict`
> Field value can be a dictionary.
>> But for now, Pydbm can not validators dict of type.
> Only validate type of the field is dict.

`float`
> Field value can be a floating point number.

`list`
> Field value can be a list.
>> But for now, Pydbm can not validators list of type.
> Only validate type of the field is list.

`set`
> Field value can be a set.
>> But for now, Pydbm can not validators set of type.
> Only validate type of the field is set.

`str`
> Field value can be a string.

`tuple`
> Field value can be a tuple.
>> But for now, Pydbm can not validators tuple of type.
> Only validate type of the field is tuple.

---

```python
from datetime import datetime, date

from pydbm import BaseModel


class User(BaseModel):
    age: bool
    avatar: bytes
    birthday: date
    created_at: datetime
    extra_data: dict
    height: float
    friends: list
    friends_set: set
    bio: str
    friends_tuple: tuple


user = User(
    age=True,
    avatar=b"avatar",
    birthday=date(2000, 1, 1),
    created_at=datetime(2021, 1, 1, 1, 1, 1),
    extra_data={"name": "hakan"},
    height=1.80,
    friends=["hakan", "ali"],
    friends_set={"hakan", "ali"},
    bio="bio",
    friends_tuple=("hakan", "ali"),
)

# >>> User(
#   age=True,
#   avatar=b'avatar',
#   birthday=datetime.date(2000, 1, 1),
#   created_at=datetime.datetime(2021, 1, 1, 1, 1, 1),
#   extra_data={'name': 'hakan'},
#   height=1.8,
#   friends=['hakan', 'ali'],
#   friends_set={'ali', 'hakan'},
#   bio='bio',
#   friends_tuple=('hakan', 'ali')
#)


user.save()

get_user = User.get(user.id)
assert get_user == user
```
