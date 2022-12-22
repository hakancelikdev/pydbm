import datetime
import dbm

import pytest

from pydbm import DbmModel
from pydbm.database import DatabaseManager


@pytest.fixture(scope="function")
def minimum_manager() -> DatabaseManager:
    minimum_manager: DbmModel = type(  # type: ignore
        "minimum_manager",
        (DbmModel,),
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
    assert minimum_manager.__database_headers__ == {"str": str}

    with minimum_manager as db:
        assert "__database_headers__" in db
        assert db["__database_headers__"] == b"{'str': 'str'}"


@pytest.mark.parametrize("annotations", [
    {
        "bool": bool,
        "bytes": bytes,
        "date": datetime.date,
        "datetime": datetime.datetime,
        "float": float,
        "int": int,
        "none": None,
        "str": str,
    },
    {
        "bool": "bool",
        "bytes": "bytes",
        "date": "datetime.date",
        "datetime": "datetime.datetime",
        "float": "float",
        "int": "int",
        "none": "None",
        "str": "str",
    },
])
def test__database_headers__maximum_manager(annotations):
    class MaximumManager(DbmModel):
        __annotations__ = annotations

    objects = MaximumManager.objects

    assert len(objects) == 1
    assert objects.__database_headers__ == {
        "bool": bool,
        "bytes": bytes,
        "date": datetime.date,
        "datetime": datetime.datetime,
        "float": float,
        "int": int,
        "none": None,
        "str": str,
    }

    with objects as db:
        assert "__database_headers__" in db
        assert (
            b"{'bool': 'bool', 'bytes': 'bytes', 'date': 'date', 'datetime': 'datetime', 'float': 'float', 'int': 'int', 'none': 'null', 'str': 'str'}"  # noqa: E501
            == db["__database_headers__"]
        )


@pytest.mark.parametrize(
    "field_type, expected_field_type, field_value",
    [
        (bool, bool, True),
        (bool, bool, False),
        (bytes, bytes, b"test"),
        (datetime.date, datetime.date, datetime.date(2021, 1, 1)),
        (datetime.datetime, datetime.datetime, datetime.datetime(2021, 1, 1, 0, 0, 0)),
        (float, float, 1.0),
        (int, int, 1),
        (None, None, None),
        (str, str, "test"),
        ("bool", bool, True),
        ("bool", bool, False),
        ("bytes", bytes, b"test"),
        ("datetime.date", datetime.date, datetime.date(2021, 1, 1)),
        ("datetime.datetime", datetime.datetime, datetime.datetime(2021, 1, 1, 0, 0, 0)),
        ("float", float, 1.0),
        ("int", int, 1),
        ("None", None, None),
        ("str", str, "test"),
    ],
)
def test_save_get_delete(teardown_db, field_type, expected_field_type, field_value):
    class SaveGetDeleteTestModel(DbmModel):
        __annotations__ = {"field": field_type}

    assert SaveGetDeleteTestModel.objects.__database_headers__ == {"field": expected_field_type}

    # save
    assert len(SaveGetDeleteTestModel.objects) == 1
    pk = SaveGetDeleteTestModel(field=field_value).pk
    SaveGetDeleteTestModel.objects.save(pk=pk, fields={"field": field_value})
    assert len(SaveGetDeleteTestModel.objects) == 2

    # get
    _model = SaveGetDeleteTestModel.objects.get(pk=pk)
    assert _model.field == field_value
    assert _model.pk == pk
    assert _model.id == pk

    # delete
    SaveGetDeleteTestModel.objects.delete(pk=pk)
    assert len(SaveGetDeleteTestModel.objects) == 1


@pytest.mark.parametrize(
    "field_type, expected_field_type, field_value, updated_value",
    [
        (bool, bool, True, False),
        (bool, bool, False, True),
        (bytes, bytes, b"test", b"new-value"),
        (datetime.date, datetime.date, datetime.date(2021, 1, 1), datetime.date(2021, 1, 2)),
        (datetime.datetime, datetime.datetime, datetime.datetime(2021, 1, 1, 0, 0, 0), datetime.datetime(2021, 1, 1, 0, 0, 1)),  # noqa: E501
        (float, float, 1.0, 2.0),
        (int, int, 1, 2),
        (None, None, None, None),
        (str, str, "test", "new-value"),
        ("bool", bool, True, False),
        ("bool", bool, False, True),
        ("bytes", bytes, b"test", b"new-value"),
        ("datetime.date", datetime.date, datetime.date(2021, 1, 1), datetime.date(2021, 1, 2)),
        ("datetime.datetime", datetime.datetime, datetime.datetime(2021, 1, 1, 0, 0, 0), datetime.datetime(2021, 1, 1, 0, 0, 1)),  # noqa: E501
        ("float", float, 1.0, 2.0),
        ("int", int, 1, 2),
        ("None", None, None, None),
        ("str", str, "test", "new-value"),
    ],
)
def test_create_update(teardown_db, field_type, expected_field_type, field_value, updated_value):
    class CreateUpdateTestModel(DbmModel):
        __annotations__ = {"field": field_type}

    assert CreateUpdateTestModel.objects.__database_headers__ == {"field": expected_field_type}

    # create
    assert len(CreateUpdateTestModel.objects) == 1
    _model = CreateUpdateTestModel.objects.create(field=field_value)
    assert len(CreateUpdateTestModel.objects) == 2
    assert _model.field == field_value

    pk = _model.pk

    # get
    assert CreateUpdateTestModel.objects.get(pk=pk).field == field_value

    # update
    CreateUpdateTestModel.objects.update(pk=pk, field=updated_value)
    assert len(CreateUpdateTestModel.objects) == 2

    # get
    assert CreateUpdateTestModel.objects.get(pk=pk).field == updated_value

    # delete
    CreateUpdateTestModel.objects.delete(pk=pk)
    assert len(CreateUpdateTestModel.objects) == 1
