import pytest

from pydbm import exceptions

all_exceptions = list(exceptions.__all__)

validation_error = all_exceptions.pop(all_exceptions.index("ValidationError"))


@pytest.mark.parametrize("exception", all_exceptions)
def test_exception_type(exception):
    """Test that all custom exceptions are instances of BaseException."""
    assert issubclass(getattr(exceptions, exception), exceptions.PydbmBaseException)
    assert isinstance(getattr(exceptions, exception)(), exceptions.PydbmBaseException)


def test_validation_error_type():
    assert issubclass(getattr(exceptions, validation_error), exceptions.PydbmBaseException)

    error = getattr(exceptions, validation_error)("field", "1", ValueError("It must be int"))
    assert isinstance(error, exceptions.PydbmBaseException)
    assert str(error) == "Invalid value for field='1'; It must be int."
