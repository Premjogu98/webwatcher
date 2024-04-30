import logging

# formatter = logging.Formatter(
#     "%(asctime)s,%(msecs)d %(levelname)-8s [camera_management: %(pathname)s:%(filename)s:%(lineno)d] %(message)s"
# )


class CustomFormatter(logging.Formatter):

    grey = "\x1b[37;20m"
    cyan = "\x1b[36;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s,%(msecs)d %(levelname)-8s [camera_management: %(pathname)s:%(filename)s:%(lineno)d] "
    message = "%(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset + message,
        logging.INFO: cyan + format + reset + message,
        logging.WARNING: yellow + format + reset + message,
        logging.ERROR: bold_red + format + reset + message,
        logging.CRITICAL: bold_red + format + reset + message,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logger(name, log_file=None, level=logging.DEBUG):
    """To setup as many loggers as you want"""
    if log_file:
        handler = logging.FileHandler(log_file)
        handler.setFormatter(CustomFormatter())
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(CustomFormatter())
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
