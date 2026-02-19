import warnings

import pytest

from pydbm import DbmModel


class Address(DbmModel):
    street: str
    city: str


class UserWithAddress(DbmModel):
    name: str
    address: Address


def test_embed_model_create(teardown_db):
    addr = Address(street="Main St", city="Istanbul")
    user = UserWithAddress(name="Hakan", address=addr)
    user.save()

    loaded = UserWithAddress.objects.get(id=user.id)
    assert loaded.name == "Hakan"
    assert isinstance(loaded.address, Address)
    assert loaded.address.street == "Main St"
    assert loaded.address.city == "Istanbul"


def test_embed_model_create_with_dict(teardown_db):
    user = UserWithAddress(name="Hakan", address={"street": "Main St", "city": "Istanbul"})
    user.save()

    loaded = UserWithAddress.objects.get(id=user.id)
    assert loaded.name == "Hakan"
    assert isinstance(loaded.address, Address)
    assert loaded.address.street == "Main St"
    assert loaded.address.city == "Istanbul"


def test_embed_model_update(teardown_db):
    addr = Address(street="Main St", city="Istanbul")
    user = UserWithAddress(name="Hakan", address=addr)
    user.save()

    new_addr = Address(street="Second St", city="Ankara")
    user.update(address=new_addr)

    loaded = UserWithAddress.objects.get(id=user.id)
    assert loaded.address.street == "Second St"
    assert loaded.address.city == "Ankara"


def test_embed_model_delete(teardown_db):
    addr = Address(street="Main St", city="Istanbul")
    user = UserWithAddress(name="Hakan", address=addr)
    user.save()

    user.delete()
    with pytest.raises(user.DoesNotExists):
        UserWithAddress.objects.get(id=user.id)


def test_embed_model_all_and_filter(teardown_db):
    user1 = UserWithAddress(name="Hakan", address=Address(street="Main St", city="Istanbul"))
    user1.save()

    user2 = UserWithAddress(name="Ali", address=Address(street="Second St", city="Ankara"))
    user2.save()

    all_users = sorted(list(UserWithAddress.objects.all()), key=lambda x: x.id)
    assert len(all_users) == 2

    filtered = list(UserWithAddress.objects.filter(name="Hakan"))
    assert len(filtered) == 1
    assert filtered[0].name == "Hakan"
    assert filtered[0].address.street == "Main St"


def test_embed_model_with_numeric_fields(teardown_db):
    class Location(DbmModel):
        lat: float
        lng: float

    class Place(DbmModel):
        name: str
        location: Location

    loc = Location(lat=41.0, lng=29.0)
    place = Place(name="Istanbul", location=loc)
    place.save()

    loaded = Place.objects.get(id=place.id)
    assert loaded.name == "Istanbul"
    assert isinstance(loaded.location, Location)
    assert loaded.location.lat == 41.0
    assert loaded.location.lng == 29.0


def test_embed_model_with_int_fields(teardown_db):
    class Dimensions(DbmModel):
        width: int
        height: int

    class Box(DbmModel):
        name: str
        dimensions: Dimensions

    dims = Dimensions(width=10, height=20)
    box = Box(name="MyBox", dimensions=dims)
    box.save()

    loaded = Box.objects.get(id=box.id)
    assert loaded.dimensions.width == 10
    assert loaded.dimensions.height == 20


def test_dict_field_warns(teardown_db):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        class ModelWithDict(DbmModel):
            name: str
            metadata: dict

        assert len(w) == 1
        assert "Consider using an embed model" in str(w[0].message)


def test_dict_field_save_and_load(teardown_db):
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")

        class ModelWithDict(DbmModel):
            name: str
            metadata: dict

    model = ModelWithDict(name="test", metadata={"key": "value", "count": 42})
    model.save()

    loaded = ModelWithDict.objects.get(id=model.id)
    assert loaded.name == "test"
    assert loaded.metadata == {"key": "value", "count": 42}


def test_embed_model_with_bool_field(teardown_db):
    class Settings(DbmModel):
        enabled: bool
        name: str

    class App(DbmModel):
        title: str
        settings: Settings

    settings = Settings(enabled=True, name="dark_mode")
    app = App(title="MyApp", settings=settings)
    app.save()

    loaded = App.objects.get(id=app.id)
    assert loaded.settings.enabled is True
    assert loaded.settings.name == "dark_mode"
