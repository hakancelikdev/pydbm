## Embed Models

Embed models allow you to use a `DbmModel` subclass as a field type in another model.
The embedded model is stored inline within the parent model's database record as a dictionary,
rather than in a separate table.

This is useful when you want to group related fields together and reuse them across models
while keeping type safety and validation.

### Basic Usage

```python
from pydbm import DbmModel


class Address(DbmModel):
    street: str
    city: str


class UserModel(DbmModel):
    name: str
    address: Address
```

You can pass an instance of the embedded model when creating the parent model:

```python
address = Address(street="Main St", city="Istanbul")
user = UserModel(name="Hakan", address=address)
user.save()
```

You can also pass a dictionary, and it will be automatically converted to the embedded model:

```python
user = UserModel(name="Hakan", address={"street": "Main St", "city": "Istanbul"})
user.save()
```

### Accessing Embedded Fields

When you retrieve a model from the database, the embedded field is returned as a model instance:

```python
loaded_user = UserModel.objects.get(id=user.id)

assert isinstance(loaded_user.address, Address)
assert loaded_user.address.street == "Main St"
assert loaded_user.address.city == "Istanbul"
```

### Updating Embedded Fields

You can update the embedded field by passing a new model instance:

```python
user = UserModel.objects.get(id=user.id)
new_address = Address(street="Second St", city="Ankara")
user.update(address=new_address)
```

### Supported Field Types in Embed Models

Embed models support all the standard [field types](field-types.md):

```python
from pydbm import DbmModel


class Location(DbmModel):
    name: str
    lat: float
    lng: float
    active: bool


class Place(DbmModel):
    title: str
    location: Location
```

### Using `dict` Instead of Embed Model

You can also use `dict` as a field type, but Pydbm will issue a warning recommending
you use an embed model instead for better type safety:

```python
from pydbm import DbmModel


# This works but will produce a warning
class UserModel(DbmModel):
    name: str
    metadata: dict
```

```python
user = UserModel(name="Hakan", metadata={"role": "admin", "level": 5})
user.save()

loaded = UserModel.objects.get(id=user.id)
assert loaded.metadata == {"role": "admin", "level": 5}
```

When using `dict`, the values must be basic Python literals (str, int, float, bool, None)
since they are serialized using `str()` and deserialized using `ast.literal_eval()`.

With embed models, all [supported field types](field-types.md) are properly serialized
and deserialized through the type system, which is why they are the recommended approach.
