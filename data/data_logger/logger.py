import logging
import sys
from logging import Logger

APP_LOGGER_NAME = 'AutoTrader2'


def setup_applevel_logger(logger_name: str = APP_LOGGER_NAME,
                          is_debug: bool = True,
                          file_name: str = None) -> Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG if is_debug else logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(sh)

    if file_name:
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def get_logger(module_name: str) -> Logger:
    return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)
