# Changelog

All notable changes to this project will be documented in this file.

## [0.7.0] - 2026-02-19

### Added

- **Model inheritance** [#29](https://github.com/hakancelikdev/pydbm/issues/29)
  - Concrete inheritance: subclasses inherit all fields from parent models; each concrete model has its own table.
  - Abstract base models: set `Config.abstract = True` to define a model that only supplies fields and optional config for subclasses (no table, no `objects`, cannot be instantiated).
  - Config inheritance: subclasses without a `Config` inherit `unique_together` from the first base that has one; table name is always derived from the subclass name.
- `model.objects.first()` — return the first record from the database, or `None` if empty.
- `model.objects.last()` — return the last record from the database, or `None` if empty.
- `model.objects.get_or_create(**kwargs)` — fetch by unique_together or create if missing; returns `(instance, created)`.
- Optional `None` for model fields [#65](https://github.com/hakancelikdev/pydbm/issues/65): fields typed as `X | None` or `Optional[X]` accept `None` and are validated/optional accordingly.

### Changed

- Performance: core manager operations optimized; `first()` and `last()` use direct key index access instead of iterating/deserializing all records.

### Fixed

- Protect `id` field from being overwritten or redefined [#55](https://github.com/hakancelikdev/pydbm/issues/55): raise `ReadOnlyFieldError` when `id` is defined in model annotations, passed to the constructor, or modified after creation.
- Wrap `self.all()` with `iter()` to satisfy mypy type checking.

### Documentation

- Embed model and dict field type documentation.
- Normalizers tutorial [#59](https://github.com/hakancelikdev/pydbm/issues/59).
- Model inheritance and Config options (including `abstract`) in models and model-config docs.
- CLAUDE.md for project guidance and architecture overview.

## [0.6.0] - 2023-07-19
### Added
- Implement exists() method [#50](https://github.com/hakancelikdev/pydbm/issues/50)

### Changed
- Add kwargs to objects.get not only take pk [#48](https://github.com/hakancelikdev/pydbm/issues/48)

### Fixed
- The database can only be opened once.
- The pk value keeps changing when using all or filter. [#51](https://github.com/hakancelikdev/pydbm/issues/51)
- Raise EmptyModelError when only defined id field in the model.

### Removed
- Pk field remove from all codebase.

## [0.5.1] - 2023-07-04
### Fixed
- Fix objects.all and filter does not work properly [#46](https://github.com/hakancelikdev/pydbm/issues/46)

## [0.5.0] - 2023-07-03

### Added
- EmptyModelError exception added
- Implement UnnecessaryParamsError [#41](https://github.com/hakancelikdev/pydbm/pull/41)
  Throw an exception when a non-existent field is entered on the model.
- Add count method to get model's data count. [#44](https://github.com/hakancelikdev/pydbm/pull/44)
  ````python
  import pydbm
  
  
  class Model(pydbm.DbmModel):
      username: str
  
  
  assert Model.objects.count() == 0
  ````


### Changed
- .db extension changed to .pydbm

### Fixed
- Fix: Update obj on DB when updating the field on the instance. [#43](https://github.com/hakancelikdev/pydbm/pull/43)
  ````python
  import pydbm
  
  
  class Model(pydbm.DbmModel):
    username: str
  
  
  model = Model(username="username")
  model.save()
  
  model.username = "new_username"
  model.save()
  
  assert Model.objects.get(id=model.id) == Model(username="new_username")
  ````

## [0.4.0] - 2022-12-23

### Added
- Support for Python3.8 [#5](https://github.com/hakancelikdev/pydbm/issues/5)
- Support date and datetime data types [#14](https://github.com/hakancelikdev/pydbm/issues/14)
- Add database manager, now database operations are as below.
  - model.objects.get
  - model.objects.create
  - model.objects.delete
  - model.objects.all
  - model.objects.filter
  - model.save
  - model.update
- Implement DoesNotExist exception under Model [#23](https://github.com/hakancelikdev/pydbm/issues/23)

### Changed
- BaseMode -> DbmModel [#24](https://github.com/hakancelikdev/pydbm/issues/24)

### Fixed
- Fix find object annotations from the model.

### Removed
- Removed some supported types
  - dict
  - list
  - set
  - tuple
- Removed some supported validation
  - validate_dict
  - validate_list
  - validate_set
  - validate_tuple

## [0.3.0] - 2022-12-04

### Added
- Support for Python3.9 [#6](https://github.com/hakancelikdev/pydbm/issues/6)
- Documentations for all features [#8](https://github.com/hakancelikdev/pydbm/issues/8)

### Changed
- Documentations improve, add version support [#11](https://github.com/hakancelikdev/pydbm/issues/11)

### Fixed
- Fix exception name -> BaseException [#12](https://github.com/hakancelikdev/pydbm/issues/12)

## [0.2.0] - 2022-11-29

### Added
- Add max_value and min_value parameters to Field, for now only support int type.
- Add more tests

### Changed
- Rename OdbmBaseException to BaseException
- Rename OdbmTypeError to PydbmTypeError
- Rename OdbmValidationError to ValidationError
- ValidationError description changes from f"{value!r} must be less than {max_value}" to f"It must be less than {max_value}"

### Removed
- BoolField
- GenericField
- BytesField
- DateField
- DateTimeField
- DictField
- Field
- FloatField
- IntField
- ListField
- NoneField
- SetField
- StrField
- TupleField
- Undefined

## [0.1.0] - 2022-11-27

### Added
- Added Meta class.
  - Auto slots
  - Field validation.
  - Database connection.
  - Primary key generation.
- Added BaseModel class.
  - Added hash method. 
  - Added eq method.
  - Added save method.
  - Added create method.
  - Added get method.
  - Added delete method.
  - Added update method.
  - Added all method.
  - Added filter method.
- Added BaseField descriptor.
  - Added field validation.
  - Added type checking.
  - Added AutoField.
  - Added BoolField.
  - Added DatetimeField.
  - Added DateField.
  - Added GenericField.
  - Added DictField.
  - Added NoneField.
  - Added IntField.
  - Added FloatField.
  - Added ListField.
  - Added TupleField.
  - Added BytesField.
  - Added StrField.
  - Added SetField.
- Added Validators.
  - validate_bool
  - validate_bytes
  - validate_date
  - validate_datetime
  - validate_dict
  - validate_float
  - validate_int
  - validate_list
  - validate_none
  - validate_set
  - validate_str
  - validate_tuple
  - validate_max_value
  - validate_min_value
- Added Databases class.
  - Added open method.
  - Added close method.
  - Added get method.
  - Added as_dict method.
  - Added db method.
  - Added keys method.
  - Added len, contains, delitem, getitem, setitem magic method.
- Added Logging.
- Added Exception classes.
  - Added BaseException.
  - Added DoesNotExists.
  - Added PydbmTypeError.
  - Added ValidationError.