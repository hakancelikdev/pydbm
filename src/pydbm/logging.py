import logging

__all__ = (
    "logger",
)

# create logger
logger = logging.getLogger("pydbm")  # unexport: public
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(
        "[%(asctime)s,%(msecs)03d %(levelname)s %(processName)s/%(threadName)s] [%(name)s:%(funcName)s:%(lineno)d] %(message)s",  # noqa: E501
        datefmt="%Y-%b-%d %H:%M:%S",
    )

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
