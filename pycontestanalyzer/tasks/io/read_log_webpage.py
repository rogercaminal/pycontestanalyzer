from typing import List, Optional
from datetime import datetime
from tempfile import TemporaryDirectory
from urllib.request import urlopen, HTTPError
import zipfile
from io import StringIO, BytesIO
import pandas as pd
import ssl

from pycontestanalyzer.base.task import Task
from pycontestanalyzer.errors.property import (
    PropertyGetterError,
    PropertySetterError,
)


class ReadLogWebpage(Task):
    def __init__(self, year: int, mode: str, callsign: str):
        super().__init__()
        self._year = year
        self._mode = mode
        self._callsign = callsign

    @property
    def year(self) -> int:
        if not isinstance(self._year, int):
            raise PropertyGetterError("year must be a string or None")
        return self._year

    @property
    def mode(self) -> str:
        if not isinstance(self._mode, str):
            raise PropertyGetterError("mode must be a string or None")
        return self._mode

    @property
    def callsign(self) -> str:
        if not isinstance(self._callsign, str):
            raise PropertyGetterError("callsign must be a string or None")
        return self._callsign

    def _read_metadata(self, log: List[str]):
        dict_metadata = dict()
        keywords = [
            "CALLSIGN",
            "LOCATION",
            "CATEGORY-OPERATOR",
            "CATEGORY-ASSISTED",
            "CATEGORY-BAND",
            "CATEGORY-POWER",
            "CATEGORY-TRANSMITTER",
            "CATEGORY-OVERLAY",
            "CLAIMED-SCORE",
            "OPERATORS",
            "CREATED-BY",
        ]
        for l in log:
            for kw in keywords:
                if kw in l:
                    dict_metadata[kw] = l.replace(f"{kw}: ", "")
        self.obj = dict_metadata

    def _read_qsos(self, log: List[str]):
        keys = {
            "freq": int,
            "mode": str,
            "date": str,
            "time": str,
            "mycall": str,
            "myrst": int,
            "myexch": int,
            "call": str,
            "urrst": int,
            "urexch": int,
            "dummy": str,
        }
        data = {k: [] for k in keys}
        for l in log:
            if "QSO: " in l:
                l = " ".join(l.replace("QSO: ", "").split())
                for k, v in zip(keys.keys(), l.split()):
                    data[k].append(v)
        self.df = pd.DataFrame(data=data).astype(keys)
        self.df.drop(columns=["dummy"], inplace=True)
        self.df["datetime"] = pd.to_datetime(
            self.df["date"] + " " + self.df["time"]
        )

    def execute(self):
        # Download log
        website_address = f"http://www.cqww.com/publiclogs/{self.year}{self.mode}/{self.callsign.lower()}.log"
        self.logger.info(f"Getting log from {website_address}")
        html = None
        try:
            context = ssl._create_unverified_context()
            with urlopen(website_address, context=context) as response:
                html = response.read()
        except HTTPError:
            self.logger.warning("Log not found")
        # Open as file
        full_log = BytesIO(html).read().decode("UTF-8").split("\n")
        self._read_metadata(log=full_log)
        self._read_qsos(log=full_log)
