import numpy as np
from pycontestanalyzer.base.task import Task
from pycontestanalyzer.errors.property import (
    PropertyGetterError,
    PropertySetterError,
)
from pycontestanalyzer.errors.dataframe.compute_band_error import ComputeBandError


class ComputeBand(Task):
    def __init__(self, name: str, col_frequency: str, band_id: bool = False):
        super().__init__()
        self._name = name
        self._col_frequency = col_frequency
        self._band_id = band_id
        if not self._band_id:
            self._dict_bands = {28000: 10, 21000: 15, 14000: 20, 7000: 40, 4000: 80, 2000: 160}
        else:
            self._dict_bands = {28000: 1, 21000: 2, 14000: 3, 7000: 4, 4000: 5, 2000: 6}

    @property
    def name(self) -> str:
        if not isinstance(self._name, str):
            raise PropertyGetterError("name must be a string")
        return self._name

    @property
    def col_frequency(self) -> str:
        if not isinstance(self._col_frequency, str):
            raise PropertyGetterError("col_frequency must be a string")
        return self._col_frequency

    def _check_columns_exist(self):
        if self.col_frequency not in self.df.columns:
            raise ComputeBandError(f"Column {self.col_frequency} does not exist in df")

    def execute(self):
        self.logger.info(f"Compute column {self.name} using frequency column {self.col_frequency} (band_id is {self._band_id})")
        self._check_columns_exist()
        self.df[self.name] = self.df[self.col_frequency].apply(np.round, args=(-3,)).map(self._dict_bands)