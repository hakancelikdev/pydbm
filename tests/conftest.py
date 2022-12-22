import contextlib

import pytest

from pydbm.database import DatabaseManager


@pytest.fixture(scope="function", autouse=True)
def teardown_db():
    yield
    for path in DatabaseManager.database_path.glob("*.db"):
        path.unlink()


@pytest.fixture(scope="session", autouse=True)
def _():
    yield

    for path in DatabaseManager.database_path.glob("*.db"):
        path.unlink()

    with contextlib.suppress(FileNotFoundError):
        DatabaseManager.database_path.rmdir()
