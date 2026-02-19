# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pydbm is a Python ORM built on top of the `dbm` standard library. It provides a Django-like model interface for small-scale projects that need simple persistent storage. The package is published as `pythonic-dbm` on PyPI and requires Python 3.9+. It has zero runtime dependencies.

## Common Commands

```bash
# Install for development
pip install -e .[tests]

# Run all tests
pytest tests -x -v --disable-warnings

# Run a single test file
pytest tests/models/test_base.py -x -v

# Run a specific test
pytest tests/models/test_base.py::TestClassName::test_method -x -v

# Run tests with coverage
python -m pytest -v --cov pydbm

# Lint (requires pre-commit installed)
pre-commit run --all-files

# Multi-version testing
tox
```

## Architecture

### Source layout: `src/pydbm/`

**Metaclass-driven model system:** `DbmModel` uses a custom metaclass `Meta` (`models/meta.py`) that does all the heavy lifting at class definition time:
- Inspects annotations to generate `__slots__` (fields are stored as `_fieldname` private attributes)
- Creates `Field`/`AutoField` descriptors for each annotated attribute
- Splits fields into required vs not-required lists
- Instantiates a `DatabaseManager` as `cls.objects` (the query interface)
- Generates per-model `DoesNotExists` and `RiskofReturningMultipleObjects` exception classes

**Field descriptors** (`models/fields/`):
- `BaseField` / `Field` (`base.py`) — Python descriptors that handle `__get__`/`__set__` with validation and normalization pipelines. Fields track values in `instance.fields` dict (for serialization) and `instance._fieldname` (for attribute access).
- `AutoField` (`auto.py`) — Primary key field that auto-generates IDs. When `unique_together` is configured, generates deterministic MD5 hash IDs from the unique fields; otherwise uses UUID4.

**Database layer** (`database/`):
- `DatabaseManager` (`manager.py`) — Wraps Python's `dbm` module. Each model gets its own `.pydbm` file under a `pydbm/` directory. Provides Django-style API: `save`, `get`, `create`, `update`, `delete`, `all`, `filter`, `exists`, `count`. Uses context manager pattern for db open/close.
- `BaseDataType` and type-specific subclasses (`data_types/`) — Serialization/deserialization registry. Each supported Python type (str, int, float, bool, bytes, date, datetime, None) has a subclass that converts to/from string representation for dbm storage. New types register via `__init_subclass__` with `data_type=` parameter.

**Validators** (`models/validators/`): Type validators (`validate_str`, `validate_int`, etc.) and comparison validators (`validate_min_value`, `validate_max_value`). The `validator_mapping` dict maps Python types to their validators; this is used by `Field.__call__` to auto-attach the correct type validator.

### Key patterns

- **Model inheritance:** Subclasses merge `__annotations__` from all model bases in `Meta.__new__`; each concrete model has its own table. `Config.abstract = True` skips creating `DatabaseManager` and prevents instantiation; subclasses can inherit `unique_together` from the first base with a Config.
- `unique_together` on a model's `Config` class controls both primary key generation (deterministic hashing) and uniqueness enforcement via `DatabaseManager.get()`.
- Data flows through: user value → normalizers → validators → descriptor `__set__` → `instance.fields` dict → `DatabaseManager.save()` → `BaseDataType.set()` → dbm file.
- Tests auto-cleanup: `conftest.py` has autouse fixtures that delete all `.pydbm` files after each test function and remove the `pydbm/` directory after the session.

## Linting & Code Style

- Line length: 120 characters
- Formatter: black, isort (profile=black)
- Pre-commit hooks: isort, unimport (removes unused imports), unexport (enforces `__all__`), mypy (excludes tests/)
- The `# unexport: not-public` comment marks module-level names that shouldn't be in `__all__`
