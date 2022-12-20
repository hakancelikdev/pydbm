import datetime as datetime

import pytest

from pydbm import BaseModel, DoesNotExists


class Model(BaseModel):
    str: str
    int: int
    float: float
    tuple: tuple
    list: list
    dict: dict
    set: set
    bool: bool
    bytes: bytes
    date: datetime.date
    datetime: datetime.datetime


def test_base_slots():
    assert BaseModel.__slots__ == ("_pk", "fields", "id")


def test_base_init():
    model = Model(
        str="str",
        int=1,
        float=1.0,
        tuple=(1, 2),
        list=[1, 2],
        dict={"a": 1},
        set={1, 2},
        bool=True,
        bytes=b"123",
        date=datetime.date(2020, 1, 1),
        datetime=datetime.datetime(2020, 1, 1, 2, 10, 40),
    )

    assert model.str == "str"
    assert model.int == 1
    assert model.float == 1.0
    assert model.tuple == (1, 2)
    assert model.list == [1, 2]
    assert model.dict == {"a": 1}
    assert model.set == {1, 2}
    assert model.bool is True
    assert model.bytes == b"123"
    assert model.date == datetime.date(2020, 1, 1)
    assert model.datetime == datetime.datetime(2020, 1, 1, 2, 10, 40)
    assert model.pk == model.id
    assert model.pk == "74e5cebd6d8f4c58d0bbb879ed4e3322"
    assert model.fields == {
        "str": "str",
        "int": 1,
        "float": 1.0,
        "tuple": (1, 2),
        "list": [1, 2],
        "dict": {"a": 1},
        "set": {1, 2},
        "bool": True,
        "bytes": b"123",
        "date": datetime.date(2020, 1, 1),
        "datetime": datetime.datetime(2020, 1, 1, 2, 10, 40),
    }


def test_base_repr():
    model = Model(
        str="str",
        int=1,
        float=1.0,
        tuple=(1, 2),
        list=[1, 2],
        dict={"a": 1},
        set={1, 2},
        bool=True,
        bytes=b"123",
        date=datetime.date(2020, 1, 1),
        datetime=datetime.datetime(2020, 1, 1, 2, 10, 40),
    )

    assert (
        repr(model)
        == "Model(str='str', int=1, float=1.0, tuple=(1, 2), list=[1, 2], dict={'a': 1}, set={1, 2}, bool=True, bytes=b'123', date=datetime.date(2020, 1, 1), datetime=datetime.datetime(2020, 1, 1, 2, 10, 40))"  # noqa: E501
    )


def test_base_eq():
    model_1 = Model(
        str="str",
        int=1,
        float=1.0,
        tuple=(1, 2),
        list=[1, 2],
        dict={"a": 1},
        set={1, 2},
        bool=True,
        bytes=b"123",
        date=datetime.date(2020, 1, 1),
        datetime=datetime.datetime(2020, 1, 1, 2, 10, 40),
    )
    model_2 = Model(
        str="str",
        int=1,
        float=1.0,
        tuple=(1, 2),
        list=[1, 2],
        dict={"a": 1},
        set={1, 2},
        bool=True,
        bytes=b"123",
        date=datetime.date(2020, 1, 1),
        datetime=datetime.datetime(2020, 1, 1, 2, 10, 40),
    )

    assert model_1 == model_2

    model_3 = Model(
        str="str",
        int=1,
        float=1.0,
        tuple=(1, 2),
        list=[1, 2],
        dict={"a": 1},
        set={1, 2},
        bool=True,
        bytes=b"12",
        date=datetime.date(2020, 1, 1),
        datetime=datetime.datetime(2020, 1, 1, 2, 10, 40),
    )
    assert model_1 != model_3
    assert model_2 != model_3


def test_base_hash():
    class Account(BaseModel):
        ids: int
        name: str

    accounts = {
        Account(ids=1, name="John"),
        Account(ids=1, name="John"),
        Account(ids=2, name="Jane"),
    }

    assert accounts == {Account(ids=1, name="John"), Account(ids=2, name="Jane")}


@pytest.mark.parametrize(
    "field_type, field_value",
    [
        (str, "str"),
        (int, 1),
        (float, 1.0),
        # (tuple, (1, 2)),
        # (list, [1, 2]),
        # (dict, {"a": 1}),
        # (set, {1, 2}),
        (bool, True),
        (bytes, b"123"),
        (datetime.date, datetime.date(2020, 1, 1)),
        (datetime.datetime, datetime.datetime(2020, 1, 1, 2, 10, 40)),
    ],
)
def test_base_save(teardown_db, field_type, field_value):
    example_model: BaseModel = type("Example", (BaseModel,), {"__annotations__": {"field": field_type}})  # type: ignore

    model = example_model(field=field_value)
    assert model.save() is None

    model = example_model.objects.get(pk=model.id)
    assert model.field == field_value


def test_base_create(teardown_db):
    class Example(BaseModel):
        str: str

    assert Example.objects.create(str="str") == Example(str="str")


def test_base_get(teardown_db):
    class Example(BaseModel):
        str: str

    model = Example.objects.create(str="str")

    assert Example.objects.get(pk=model.pk) == model


def test_base_delete(teardown_db):
    class Example(BaseModel):
        str: str

    model = Example.objects.create(str="str")

    model.delete()
    with pytest.raises(DoesNotExists) as cm:
        Example.objects.get(pk=model.id)
    assert str(cm.value) == "Example with pk 341be97d9aff90c9978347f66f945b77 does not exists"


def test_base_update(teardown_db):
    class Example(BaseModel):
        str: str

    model = Example.objects.create(str="str")
    model.update(str="new_str")

    assert model.str == "new_str"
    assert Example.objects.get(pk=model.pk).str == "new_str"


def test_base_all(teardown_db):
    class Example(BaseModel):
        str: str

    assert Example.objects.create(str="str") == Example(str="str")
    assert Example.objects.create(str="another str") == Example(str="another str")

    assert list(Example.objects.all()) == [Example(str="another str"), Example(str="str")]


def test_base_filter(teardown_db):
    class Example(BaseModel):
        str: str

    Example.objects.create(str="str")
    Example.objects.create(str="another str")

    assert list(Example.objects.filter(str="str")) == [Example(str="str")]
