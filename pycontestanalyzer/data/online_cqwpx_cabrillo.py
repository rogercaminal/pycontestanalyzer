"""CQ WW Contest cabrillo data source module."""
from os import PathLike
from typing import Any, ClassVar, Optional, Union

from pandas import DataFrame, to_datetime

from pycontestanalyzer.data.online_contest_cabrillo import (
    OnlineContestCabrilloDataSource
)


class OnlineCQWPXCabrilloDataSource(OnlineContestCabrilloDataSource):
    """CQ WPX Contest cabrillo data source definition."""

    path: ClassVar[Union[str, PathLike]] = "{year}{mode}/{callsign}.log"
    prefix: Optional[str] = "http://www.cqwpx.com/publiclogs/"
    dtypes: dict[str, str] = {
        "frequency": "int",
        "mode": "str",
        "date": "str",
        "time": "str",
        "mycall": "str",
        "myrst": "int",
        "myserial": "int",
        "call": "str",
        "rst": "int",
        "serial": "int",
        "radio": "int",
    }

    def __init__(
        self,
        callsign: str,
        year: int,
        mode: str,
    ):
        """Online contest cabrillo data source constructor.

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
        super().__init__(callsign=callsign, year=year, mode=mode)

    def process_result(self, data: DataFrame) -> DataFrame:
        """Processes Performance output loaded data."""
        data.columns = list(self.dtypes.keys())
        data = (
            data
            .assign(
                datetime=lambda x: to_datetime(
                    x["date"] + " " + x["time"], 
                    format="%Y-%m-%d %H%M"
                ),
                # band=lambda x: x.apply()
            )
            .drop(columns=["date", "time"])
        )
        return data
