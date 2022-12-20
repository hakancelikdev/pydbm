# Pydbm

**Pydbm is a more pythonic way to use dbm.**

[![pre-commit](https://github.com/hakancelikdev/pydbm/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/hakancelikdev/pydbm/actions/workflows/pre-commit.yml)
[![test](https://github.com/hakancelikdev/pydbm/actions/workflows/tests.yml/badge.svg)](https://github.com/hakancelikdev/pydbm/actions/workflows/tests.yml)
[![build-docs](https://github.com/hakancelikdev/pydbm/actions/workflows/docs.yml/badge.svg)](https://github.com/hakancelikdev/pydbm/actions/workflows/docs.yml)
[![publish-package-on-pypi](https://github.com/hakancelikdev/pydbm/actions/workflows/pypi.yml/badge.svg)](https://github.com/hakancelikdev/pydbm/actions/workflows/pypi.yml)

[![Pypi](https://img.shields.io/pypi/v/pythonic-dbm)](https://pypi.org/project/pythonic-dbm/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pythonic-dbm)
[![Downloads](https://static.pepy.tech/personalized-badge/pythonic-dbm?period=total&units=international_system&left_color=grey&right_color=red&left_text=downloads)](https://pepy.tech/project/pythonic-dbm)
[![License](https://img.shields.io/github/license/hakancelikdev/pydbm.svg)](https://github.com/hakancelikdev/pydbm/blob/main/LICENSE)

[![Forks](https://img.shields.io/github/forks/hakancelikdev/pydbm)](https://github.com/hakancelikdev/pydbm/fork)
[![Issues](https://img.shields.io/github/issues/hakancelikdev/pydbm)](https://github.com/hakancelikdev/pydbm/issues)
[![Stars](https://img.shields.io/github/stars/hakancelikdev/pydbm)](https://github.com/hakancelikdev/pydbm/stargazers)

[![Codecov](https://codecov.io/gh/hakancelikdev/pydbm/branch/main/graph/badge.svg)](https://codecov.io/gh/hakancelikdev/pydbm)
[![Contributors](https://img.shields.io/github/contributors/hakancelikdev/pydbm)](https://github.com/hakancelikdev/pydbm/graphs/contributors)
[![Last Commit](https://img.shields.io/github/last-commit/hakancelikdev/pydbm.svg)](https://github.com/hakancelikdev/pydbm/commits/main)

-----

It provides a fast, simple, and convenient facility for your small-scale Python projects that need a database.

Here is a quick example;

```python
from pydbm import BaseModel

__all__ = ["UserModel"]


class UserModel(BaseModel):
    name: str
    surname: str
    age: int
    username: str

    class Meta:
        unique_together = ("username", )

    def get_fullname(self) -> str:
        return f"{self.name} {self.surname}"


user = UserModel(name="Hakan", surname="Celik", age=26, username="hakancelik")
user.save()

hakan_user = UserModel.objects.get(id=user.id)

assert hakan_user.name == "Hakan"
assert hakan_user.surname == "Celik"
assert hakan_user.age == 26
assert hakan_user.username == "hakancelik"
```

