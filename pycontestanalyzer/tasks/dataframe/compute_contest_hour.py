import numpy as np
from pycontestanalyzer.base.task import Task
from pycontestanalyzer.errors.property import (
    PropertyGetterError,
    PropertySetterError,
)
from pycontestanalyzer.errors.dataframe.compute_contest_hour_error import ComputeContestHourError


class ComputeContestHour(Task):
    def __init__(self, name: str, col_datetime: str):
        super().__init__()
        self._name = name
        self._col_datetime = col_datetime

    @property
    def name(self) -> str:
        if not isinstance(self._name, str):
            raise PropertyGetterError("name must be a string")
        return self._name

    @property
    def col_datetime(self) -> str:
        if not isinstance(self._col_datetime, str):
            raise PropertyGetterError("col_datetime must be a string")
        return self._col_datetime

    def _check_columns_exist(self):
        if self.col_datetime not in self.df.columns:
            raise ComputeBandError(f"Column {self.col_datetime} does not exist in df")

    def execute(self):
        self.logger.info(f"Compute column {self.name} using datetime column {self.col_datetime}")
        self._check_columns_exist()
        self.df[self.name] = self.df[self.col_datetime].dt.hour + 24 * (self.df[self.col_datetime].dt.day - self.df[self.col_datetime].dt.day[0])