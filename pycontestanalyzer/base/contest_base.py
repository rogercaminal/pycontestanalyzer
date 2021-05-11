from abc import abstractmethod
from typing import Optional, Dict, Any, List
import pandas as pd

from pycontestanalyzer.base.object_base import ObjectBase
from pycontestanalyzer.base.task_manager import TaskManager


class ContestBase(ObjectBase):
    def __init__(
        self,
        callsign: str,
        mode: str,
        year: int,
        output_folder: Optional[str] = None,
    ):
        super().__init__()
        self._callsign = callsign
        self._mode = mode
        self._year = year

        self._output_folder = output_folder
        self._metadata: Dict[str, Any] = dict()

        self._task_manager: TaskManager = TaskManager()

    @property
    def callsign(self) -> str:
        if not isinstance(self._callsign, str):
            raise TypeError("callsign must be a string")
        return self._callsign

    @property
    def mode(self) -> str:
        if not isinstance(self._mode, str):
            raise TypeError("mode must be a string")
        return self._mode

    @property
    def year(self) -> int:
        if not isinstance(self._year, int):
            raise TypeError("year must be an int")
        return self._year

    @property
    def output_folder(self) -> str:
        if not isinstance(self._output_folder, str):
            raise TypeError("output_folder must be a string")
        return self._output_folder

    @property
    def metadata(self) -> Dict[str, Any]:
        if not isinstance(self._metadata, dict):
            raise TypeError("metadata must be a dictionary")
        keys = list(self._metadata.keys())
        if all([isinstance(k, str) for k in keys]):
            return self._metadata
        raise TypeError("keys of metadata dict must be strings")

    @metadata.setter
    def metadata(self, new_metadata: Dict[str, Any]):
        if not isinstance(new_metadata, dict):
            raise TypeError("metadata must be a dictionary")
        self._metadata = new_metadata

    @property
    def task_manager(self) -> TaskManager:
        """Task manager object property that will hold the tasks to be
        executed for this command.
        :raises PropertyGetterError: no task manager defined.
        :return: task manager
        :rtype: TaskManager
        """
        if self._task_manager is None:
            raise NameError("No task manager defined")
        return self._task_manager


# TODO AS TASKS!


# @abstractmethod
# def import_log(self):
#     ...


# self.output_folder = output_folder
# self.force_csv = force_csv

# self.cat_contest = ""
# self.cat_operator = ""
# self.cat_assisted = ""
# self.cat_band = ""
# self.cat_power = ""
# self.cat_transmitter = ""
# self.category = ""
# self.operator_names = ""
# self.location = ""
# self.operators = []
# self.club = ""
# self.log = None
# self.rbspots = None

# self.save = False

# self.log_path = ""
# self.log_name = ""

# self.max_rates = {}
# self.rates_per_minute = []

# self.call_exists, self.download_ok = self.import_log()
# self.download_spots_ok = self.import_reverse_beacon_spots()
