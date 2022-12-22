# Pydbm

**Pydbm is a more pythonic way to use dbm.**
> It provides a fast, simple, and convenient facility for your small-scale Python projects that need a database.

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

## Installation

Pydbm requires Python 3.8+ and can be easily installed using most common Python
packaging tools. We recommend installing the latest stable release from PyPI with pip:

```shell
$ pip install pythonic-dbm
```

----
Pydbm is a database management system that uses the dbm standard library from Python to provide interfaces to Unix databases in a pythonic way.
It is designed for small-scale projects and is a light database, meaning it is not as feature-rich or powerful as other types of databases, such as relational databases.

Pydbm is particularly useful for applications that need to store and retrieve simple data structures quickly,
and is well-suited for developers working on small-scale projects that do not require the full functionality of a more complex database management system.

Pydbm is also an object-relational mapper (ORM), which allows developers to work with their database using objects and classes rather than raw commands.
This can make it easier to manage and interact with the database in their application in a more pythonic way.

**Here is a quick example;**

```python
from pydbm import DbmModel

__all__ = (
    "UserModel",
)


class UserModel(DbmModel):
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

