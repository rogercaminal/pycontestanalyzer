"""Contest cabrillo data source module."""
from os import path, PathLike
from typing import Any, ClassVar, Mapping, Union

from pandas import DataFrame

from pycontestanalyzer.config import get_settings
from pycontestanalyzer.data.storage_source import StorageDataSource


import re
from urllib.request import urlopen
from io import StringIO


class ProcessedContestDataSource(StorageDataSource):
    """Processed contest data source definition."""

    file_format: ClassVar[str] = "parquet"
    storage_options: ClassVar[Mapping[str, Any]] = {}
    path: ClassVar[Union[str, PathLike]] = "data.parquet"

    def __init__(
        self,
        callsign: str,
        contest: str,
        year: int,
        mode: str,
    ):
        """Processed contest cabrillo data source constructor.

        The constructor can be provided with optional values to filter loaded data, such
        as geographic granularity and prediciton model (name), either a single value or
        a list. In addition, the prefix to prepend the data source path is passed to
        the parent class StorageDataSource constructor.

        Args:
            geographic_granularity: string or list of strings with geographic
                granularities to load. Defaults to None to load all data available.
            prediction_model: string or list of strings with name of the prediction
                model(s) to load. Defaults to None to load all data available.
            prefix: string with prefix to prepend the data source's path. Passed down
                to the parent StorageDataSource constructor. Defaults to None to avoid
                prepending.
        """
        settings = get_settings()
        prefix_data = settings.storage.paths.raw_data
        prefix_meta = settings.storage.paths.raw_metadata

        # super().__init__(prefix=self.prefix)
        self.callsign = callsign
        self.contest = contest
        self.year = year
        self.mode = mode
        self.path_data = (
            self.path if prefix_data is None else path.join(prefix_data, self.path)
        ).format(
            callsign=self.callsign, 
            contest=self.contest, 
            year=self.year, 
            mode=self.mode
        )
        self.path_meta = (
            self.path if prefix_meta is None else path.join(prefix_meta, self.path)
        ).format(
            callsign=self.callsign,
            contest=self.contest, 
            year=self.year, 
            mode=self.mode
        )

    def load(self) -> DataFrame:
        _data = self.read(
            file_format=self.file_format, path=self.path_data, **self.storage_options
        )
        _metadata = self.read(
            file_format=self.file_format, path=self.path_meta, **self.storage_options
        )
        _data.attrs = _metadata.to_dict()["value"]
        return _data