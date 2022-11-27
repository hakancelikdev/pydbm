import dbm

import pytest

from pydbm.database import Database


def test_database_open_remove():
    db = Database("test")
    db.open()
    db.remove()


def test_database_db_as_context_manager():
    db = Database("test").db

    assert hasattr(db, "__enter__")
    assert hasattr(db, "__exit__")


def test_database_db_close():
    with Database("test").db as db:
        pass

    with pytest.raises(dbm.error) as cm:
        db["test"] = "test"
    assert str(cm.value) == "GDBM object has already been closed"


def test_database_db_contains():
    with Database("test").db as db:
        db["test"] = "test"

        assert "test" in db


def test_database_db_add_read_delete():
    with Database("test").db as db:
        db["str"] = "str"
        db["int"] = 1
        db["float"] = 1.1
        db["list"] = [1, 2, 3]
        db["dict"] = {"a": 1, "b": 2, "c": 3}

        assert "str" == db["str"]
        assert 1 == db["int"]
        assert 1.1 == db["float"]
        assert [1, 2, 3] == db["list"]
        assert {"a": 1, "b": 2, "c": 3} == db["dict"]

        del db["str"]
        del db["int"]
        del db["float"]
        del db["list"]
        del db["dict"]

        assert "str" not in db
        assert "int" not in db
        assert "float" not in db
        assert "list" not in db
        assert "dict" not in db


def test_database_db_len():
    with Database("test").db as db:
        assert 0 == len(db)
        db["str"] = "str"
        assert 1 == len(db)
        db["int"] = 1
        assert 2 == len(db)
        db["float"] = 1.1
        assert 3 == len(db)
        db["list"] = [1, 2, 3]
        assert 4 == len(db)
        db["dict"] = {"a": 1, "b": 2, "c": 3}
        assert 5 == len(db)


def test_database_as_dict():
    with Database("test").db as db:
        db["str"] = "str"
        db["int"] = 1
        db["float"] = 1.1
        db["list"] = [1, 2, 3]
        db["dict"] = {"a": 1, "b": 2, "c": 3}

        assert {
            "str": "str",
            "int": 1,
            "float": 1.1,
            "list": [1, 2, 3],
            "dict": {"a": 1, "b": 2, "c": 3},
        } == db.as_dict()


def test_database_get():
    with Database("test").db as db:
        db["str"] = "str"
        db["int"] = 1
        db["float"] = 1.1
        db["list"] = [1, 2, 3]
        db["dict"] = {"a": 1, "b": 2, "c": 3}

        assert "str" == db.get("str")
        assert 1 == db.get("int")
        assert 1.1 == db.get("float")
        assert [1, 2, 3] == db.get("list")
        assert {"a": 1, "b": 2, "c": 3} == db.get("dict")

        assert None is db.get("default", None)
