"""Tests for model inheritance (abstract base and concrete inheritance)."""

import pytest

from pydbm import DbmModel


def test_concrete_inheritance_fields_and_slots():
    """Subclass inherits parent fields; slots and annotations are merged."""

    class Animal(DbmModel):
        name: str

    class Dog(Animal):
        breed: str

    assert "name" in Dog.__annotations__
    assert "breed" in Dog.__annotations__
    assert "id" in Dog.__annotations__
    assert "_name" in Dog.__slots__
    assert "_breed" in Dog.__slots__
    assert "_id" in Dog.__slots__
    assert Dog.required_fields == ["name", "breed"]


def test_concrete_inheritance_save_get(teardown_db):
    """Inherited model has its own table and persists all fields (base + own)."""

    class Animal(DbmModel):
        name: str

    class Dog(Animal):
        breed: str

    dog = Dog(name="Max", breed="Labrador")
    dog.save()
    assert dog.id is not None
    assert dog.name == "Max"
    assert dog.breed == "Labrador"

    loaded = Dog.objects.get(id=dog.id)
    assert loaded.name == "Max"
    assert loaded.breed == "Labrador"
    assert loaded.id == dog.id


def test_concrete_inheritance_own_table(teardown_db):
    """Subclass uses its own table name (e.g. dogs, not animals)."""

    class Animal(DbmModel):
        name: str

    class Dog(Animal):
        breed: str

    assert Dog.objects.table_name == "dogs"
    Dog(name="A", breed="B").save()
    assert Animal.objects.count() == 0
    assert Dog.objects.count() == 1


def test_abstract_base_cannot_instantiate():
    """Abstract model raises when instantiated."""

    class AbstractAnimal(DbmModel):
        name: str

        class Config:
            abstract = True

    with pytest.raises(TypeError) as exc_info:
        AbstractAnimal(name="x")
    assert "Cannot instantiate abstract model" in str(exc_info.value)
    assert "AbstractAnimal" in str(exc_info.value)


def test_abstract_base_concrete_subclass_has_all_fields(teardown_db):
    """Concrete subclass of abstract model has base + own fields and works as normal."""

    class AbstractAnimal(DbmModel):
        name: str

        class Config:
            abstract = True

    class Dog(AbstractAnimal):
        breed: str

    assert AbstractAnimal.objects is None
    dog = Dog(name="Max", breed="Labrador")
    dog.save()
    loaded = Dog.objects.get(id=dog.id)
    assert loaded.name == "Max"
    assert loaded.breed == "Labrador"


def test_abstract_base_subclass_inherits_config():
    """Subclass without Config inherits unique_together from abstract base."""

    class AbstractAnimal(DbmModel):
        name: str

        class Config:
            abstract = True
            unique_together = ("name",)

    class Dog(AbstractAnimal):
        breed: str

    # Subclass gets its own table name, inherited unique_together
    assert Dog._config.unique_together == ("name",)
    assert Dog.objects.table_name == "dogs"


def test_inheritance_empty_subclass_not_allowed():
    """Subclass that adds no fields is still valid (inherits parent fields)."""

    class Animal(DbmModel):
        name: str

    class Dog(Animal):
        pass

    # Dog has only inherited 'name' (+ id), which is valid
    assert Dog.required_fields == ["name"]
    assert "name" in Dog.__annotations__


def test_inheritance_three_levels(teardown_db):
    """Three-level inheritance: base -> middle -> leaf; leaf has all fields."""

    class Animal(DbmModel):
        name: str

    class Mammal(Animal):
        legs: int

    class Dog(Mammal):
        breed: str

    assert Dog.required_fields == ["name", "legs", "breed"]
    dog = Dog(name="Max", legs=4, breed="Labrador")
    dog.save()
    loaded = Dog.objects.get(id=dog.id)
    assert loaded.name == "Max"
    assert loaded.legs == 4
    assert loaded.breed == "Labrador"


def test_abstract_with_concrete_subclass_config_override():
    """Concrete subclass can override Config (e.g. unique_together)."""

    class AbstractAnimal(DbmModel):
        name: str

        class Config:
            abstract = True
            unique_together = ("name",)

    class Dog(AbstractAnimal):
        breed: str

        class Config:
            unique_together = ("name", "breed")

    assert Dog._config.unique_together == ("name", "breed")


def test_config_abstract_default():
    """Config without abstract defaults to abstract=False."""
    from pydbm.models import meta

    config = meta.Config(table_name="users", unique_together=())
    assert config.abstract is False
