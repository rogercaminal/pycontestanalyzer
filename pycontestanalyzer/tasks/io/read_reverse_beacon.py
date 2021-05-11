from typing import List, Optional
from datetime import datetime
from tempfile import TemporaryDirectory
from urllib.request import urlopen
import zipfile
from io import StringIO
import pandas as pd

from pycontestanalyzer.base.task import Task
from pycontestanalyzer.errors.property import PropertyGetterError


class ReadReverseBeacon(Task):
    def __init__(self, dates: List[datetime], callsign: Optional[str] = None):
        super().__init__()
        self._dates = dates
        self._callsign = callsign

    @property
    def dates(self) -> List[datetime]:
        if isinstance(self._dates, list):
            if all([isinstance(d, datetime) for d in self._dates]):
                return self._dates
        raise PropertyGetterError("dates must be a list of datetime objects")

    @property
    def callsign(self) -> Optional[str]:
        if self._callsign is None:
            return self._callsign
        elif isinstance(self._callsign, str):
            return self._callsign
        else:
            raise PropertyGetterError("callsign must be a string or None")

    def execute(self):
        spots_list = []
        tmp_dir = TemporaryDirectory().name
        with TemporaryDirectory() as tmp_dir:
            for date in self.dates:
                date_str = date.strftime("%Y%m%d")
                zip_name = f"date_{date_str}.zip"
                try:
                    website_address = (
                        "http://reversebeacon.net/raw_data/dl.php?f={}".format(
                            date_str
                        )
                    )
                    with urlopen(website_address) as response:
                        html = response.read()
                        f = open("{}/spots_{}".format(tmp_dir, zip_name), "wb")
                        f.write(html)
                        f.close()
                except:
                    logging.error("Problem getting reverse beacon spots")
                    return False
                myzipfile = zipfile.ZipFile(
                    "{}/spots_{}".format(tmp_dir, zip_name)
                )
                csvfile = [
                    myzipfile.read(name) for name in myzipfile.namelist()
                ]
                sp = pd.read_csv(StringIO(csvfile[0].decode("utf-8")))
                if self.callsign is not None:
                    sp = sp[(sp["dx"] == self.callsign)]
                sp.dropna(inplace=True)
                spots_list.append(sp)
            df_spots = pd.concat(spots_list, sort=False)
            # dtypes
            df_spots["freq"] = df_spots["freq"].astype(float)
            df_spots["band"] = (
                df_spots["band"]
                .str.split("(\d+)", expand=True)
                .values[:, 1]
                .astype(int)
            )
            df_spots["db"] = df_spots["db"].astype(int)
            df_spots["speed"] = df_spots["speed"].astype(int)
            df_spots["date"] = pd.to_datetime(df_spots["date"])
            # index
            df_spots.set_index(keys=["date"], inplace=True)
            self.df = df_spots
