from pydbm.models.base import BaseModel


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


def test_base_slots():
    assert BaseModel.__slots__ == ("fields", "id")


def test_base_init():
    model = Model(
        str="str", int=1, float=1.0, tuple=(1, 2), list=[1, 2], dict={"a": 1}, set={1, 2}, bool=True, bytes=b"123"
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
    assert model.pk == model.id
    assert model.pk == "f1222e99027b001f3699e84da444d596"
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
    }


def test_base_repr():
    model = Model(
        str="str", int=1, float=1.0, tuple=(1, 2), list=[1, 2], dict={"a": 1}, set={1, 2}, bool=True, bytes=b"123"
    )

    assert (
        repr(model)
        == "Model(str='str', int=1, float=1.0, tuple=(1, 2), list=[1, 2], dict={'a': 1}, set={1, 2}, bool=True, bytes=b'123')"  # noqa: E501
    )


def test_base_eq():
    model_1 = Model(
        str="str", int=1, float=1.0, tuple=(1, 2), list=[1, 2], dict={"a": 1}, set={1, 2}, bool=True, bytes=b"123"
    )
    model_2 = Model(
        str="str", int=1, float=1.0, tuple=(1, 2), list=[1, 2], dict={"a": 1}, set={1, 2}, bool=True, bytes=b"123"
    )

    assert model_1 == model_2

    model_3 = Model(
        str="str", int=1, float=1.0, tuple=(1, 2), list=[1, 2], dict={"a": 1}, set={1, 2}, bool=True, bytes=b"12"
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


def test_base_save():
    class Example(BaseModel):
        str: str

    assert Example(str="str").save() is None


def test_base_create():
    class Example(BaseModel):
        str: str

    assert Example.create(str="str") == Example(str="str")


def test_base_get():
    class Example(BaseModel):
        str: str

    model = Example.create(str="str")

    assert Example.get(id=model.id) == model


def test_base_delete():
    class Example(BaseModel):
        str: str

    model = Example.create(str="str")

    model.delete()
    assert Example.get(id=model.id) is None


def test_base_update():
    class Example(BaseModel):
        str: str

    model = Example.create(str="str")
    model.update(str="new_str")

    assert model.str == "new_str"
    assert Example.get(id=model.id).str == "new_str"


def test_base_all():
    class Example(BaseModel):
        str: str

    Example.create(str="str")
    Example.create(str="another str")

    assert list(Example.all()) == [Example(str="str"), Example(str="another str")]


def test_base_filter():
    class Example(BaseModel):
        str: str

    Example.create(str="str")
    Example.create(str="another str")

    assert list(Example.filter(str="str")) == [Example(str="str")]
