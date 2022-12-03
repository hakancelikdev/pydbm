# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - YYYY-MM-DD


## [0.3.0] - 2022-12-DD

### Added
- Support for Python3.9 [#6](https://github.com/hakancelikdev/pydbm/issues/6)

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