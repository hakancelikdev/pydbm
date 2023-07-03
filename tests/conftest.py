import contextlib

import pytest

from pydbm.database.manager import DATABASE_EXTENSION, DATABASE_PATH


@pytest.fixture(scope="function", autouse=True)
def teardown_db():
    yield
    for path in DATABASE_PATH.glob(f"*.{DATABASE_EXTENSION}"):
        path.unlink()


@pytest.fixture(scope="session", autouse=True)
def _():
    yield

    for path in DATABASE_PATH.glob(f"*.{DATABASE_EXTENSION}"):
        path.unlink()

    with contextlib.suppress(FileNotFoundError):
        DATABASE_PATH.rmdir()
