import logging
from pycontestanalyzer.utils.logger import get_logger
from abc import ABC, abstractmethod


class ObjectBase(ABC):
    def __init__(self):
        self._logger = get_logger("pycontestanalyzer")

    @property
    def logger(self) -> logging.Logger:
        if not isinstance(self._logger, logging.Logger):
            raise TypeError("logger must be of class logging.Logger")
        return self._logger

    @logger.setter
    def logger(self, new_logger: logging.Logger):
        if not isinstance(new_logger, logging.Logger):
            raise TypeError("logger must be of class logging.Logger")
        self._logger = new_logger

    def clear(self):
        self.__init__()

    @abstractmethod
    def execute(self):
        ...
