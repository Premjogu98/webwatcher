import logging

formatter = logging.Formatter(
    "%(asctime)s,%(msecs)d %(levelname)-8s [backend/api/%(filename)s:%(lineno)d] %(message)s"
)


def setup_logger(name, log_file=None, level=logging.DEBUG):
    """To setup as many loggers as you want"""
    if log_file:
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


console_logger = setup_logger("camera_management_console_logger")


def function_logger(func):
    """Logger for displaying function logs"""

    def inner(*args, **kwargs):
        console_logger.info(f"Called func {func.__name__}")
        console_logger.debug(f"Called func {func.__name__} with {args, kwargs}")
        ret = func(*args, **kwargs)
        console_logger.info(f"Returned func {func.__name__}")
        console_logger.debug(f"Returned func {func.__name__} returns {ret}")
        return ret

    return inner


def method_logger(method):
    """Logger for displaying method logs"""

    def inner(self, *args, **kwargs):
        console_logger.info(f"Called method {method.__name__} of {self}")
        console_logger.debug(
            f"Called method {method.__name__} of {self} with {args, kwargs}"
        )
        ret = method(self, *args, **kwargs)
        console_logger.info(f"Returned method {method.__name__} of {self}")
        console_logger.debug(
            f"Returned method {method.__name__} of {self} returns {ret}"
        )
        return ret

    return inner
