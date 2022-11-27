import pytest

from pydbm.logging import logger


def test_logger_conf():
    assert logger.name == "pydbm"
    assert logger.level == 10
    assert logger.handlers


def test_logger_format():
    assert (
        logger.handlers[0].formatter._fmt
        == "[%(asctime)s,%(msecs)03d %(levelname)s %(processName)s/%(threadName)s] [%(name)s:%(funcName)s:%(lineno)d] %(message)s"  # noqa: E501
    )  # noqa: E501
    assert logger.handlers[0].formatter.datefmt == "%Y-%b-%d %H:%M:%S"


@pytest.mark.parametrize(
    "log_name, log_value",
    [
        ("DEBUG", 10),
        ("INFO", 20),
        ("WARNING", 30),
        ("ERROR", 40),
        ("CRITICAL", 50),
    ],
)
def test_logger_info(log_name, log_value, caplog):
    caplog.set_level(log_value)
    getattr(logger, log_name.lower())("test")

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == log_name
    assert caplog.records[0].message == "test"
