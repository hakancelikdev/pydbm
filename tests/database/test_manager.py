import datetime
import dbm

import pytest

from pydbm import BaseModel
from pydbm.database import DatabaseManager


@pytest.fixture(scope="function")
def minimum_manager() -> DatabaseManager:
    minimum_manager: BaseModel = type(  # type: ignore
        "minimum_manager",
        (BaseModel,),
        {
            "__annotations__": {"str": str},
        },
    )
    return minimum_manager.objects


def test_init(minimum_manager):
    assert minimum_manager.table_name == "minimum_managers"
    assert minimum_manager.db_path.as_posix() == "pydbm/minimum_managers.db"


def test_context_manager(minimum_manager):
    assert hasattr(minimum_manager, "__enter__")
    assert hasattr(minimum_manager, "__exit__")


def test_close(minimum_manager):
    with minimum_manager as db:
        pass

    with pytest.raises(dbm.error) as cm:
        db["test"] = {}
    assert str(cm.value) == "GDBM object has already been closed"


def test__database_headers__minimum_manager(minimum_manager):
    assert len(minimum_manager) == 1
    assert minimum_manager.__database_headers__ == {"str": "str"}

    with minimum_manager as db:
        assert "__database_headers__" in db
        assert db["__database_headers__"] == b"{'str': 'str'}"


def test__database_headers__maximum_manager():
    maximum_manager: BaseModel = type(  # type: ignore
        "maximum_manager",
        (BaseModel,),
        {
            "__annotations__": {
                "bool": bool,
                "bytes": bytes,
                "date": datetime.date,
                "datetime": datetime.datetime,
                "float": float,
                "int": int,
                "noneType": type(None),
                "str": str,
            },
        },
    )
    objects = maximum_manager.objects

    assert len(objects) == 1
    assert objects.__database_headers__ == {
        "bool": "bool",
        "bytes": "bytes",
        "date": "date",
        "datetime": "datetime",
        "float": "float",
        "int": "int",
        "noneType": "NoneType",
        "str": "str",
    }

    with objects as db:
        assert "__database_headers__" in db
        assert (
            b"{'bool': 'bool', 'bytes': 'bytes', 'date': 'date', 'datetime': 'datetime', 'float': 'float', 'int': 'int', 'noneType': 'NoneType', 'str': 'str'}"  # noqa: E501
            == db["__database_headers__"]
        )


@pytest.mark.parametrize(
    "field_type, field_value",
    [
        (bool, True),
        (bool, False),
        (bytes, b"test"),
        (datetime.date, datetime.date(2021, 1, 1)),
        (datetime.datetime, datetime.datetime(2021, 1, 1, 0, 0, 0)),
        (float, 1.0),
        (int, 1),
        (type(None), None),
        (str, "test"),
    ],
)
def test_save_get_delete(teardown_db, field_type, field_value):
    model: BaseModel = type(  # type: ignore
        "SaveGetDeleteTestModel",
        (BaseModel,),
        {
            "__annotations__": {"field": field_type},
        },
    )
    assert model.objects.__database_headers__ == {"field": field_type.__name__}

    # save
    assert len(model.objects) == 1
    pk = model(field=field_value).pk
    model.objects.save(pk=pk, fields={"field": field_value})
    assert len(model.objects) == 2

    # get
    _model = model.objects.get(pk=pk)
    assert _model.field == field_value
    assert _model.pk == pk
    assert _model.id == pk

    # delete
    model.objects.delete(pk=pk)
    assert len(model.objects) == 1


@pytest.mark.parametrize(
    "field_type, field_value, updated_value",
    [
        (bool, True, False),
        (bool, False, True),
        (bytes, b"test", b"new-value"),
        (datetime.date, datetime.date(2021, 1, 1), datetime.date(2021, 1, 2)),
        (datetime.datetime, datetime.datetime(2021, 1, 1, 0, 0, 0), datetime.datetime(2021, 1, 1, 0, 0, 1)),
        (float, 1.0, 2.0),
        (int, 1, 2),
        (type(None), None, None),
        (str, "test", "new-value"),
    ],
)
def test_create_update(teardown_db, field_type, field_value, updated_value):
    model: BaseModel = type(  # type: ignore
        "CreateUpdateTestModel",
        (BaseModel,),
        {
            "__annotations__": {"field": field_type},
        },
    )
    assert model.objects.__database_headers__ == {"field": field_type.__name__}

    # create
    assert len(model.objects) == 1
    _model = model.objects.create(field=field_value)
    assert len(model.objects) == 2
    assert _model.field == field_value

    pk = _model.pk

    # get
    assert model.objects.get(pk=pk).field == field_value

    # update
    model.objects.update(pk=pk, field=updated_value)
    assert len(model.objects) == 2

    # get
    assert model.objects.get(pk=pk).field == updated_value

    # delete
    model.objects.delete(pk=pk)
    assert len(model.objects) == 1
