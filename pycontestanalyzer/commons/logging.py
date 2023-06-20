"""ALMO Logging utilities module."""
from logging.config import dictConfig

from pycontestanalyzer.config import get_settings


def config_logging():
    """Config logging through app settings."""
    dictConfig(get_settings().logging.dict())
