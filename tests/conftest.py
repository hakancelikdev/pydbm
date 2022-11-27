import pytest

from pydbm.database import Database


@pytest.fixture(scope="function", autouse=True)
def teardown_db():
    db = Database("test")
    try:
        db.remove()
    except FileNotFoundError:
        pass
