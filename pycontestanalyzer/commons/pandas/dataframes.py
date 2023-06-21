from datetime import timedelta
from logging import getLogger

import numpy as np
import pandas as pd

from pycontestanalyzer.utils import BANDMAP
from pyhamtools import Callinfo, LookupLib
from pyhamtools.locator import (
    calculate_distance,
    calculate_distance_longpath,
    calculate_heading,
    calculate_heading_longpath,
    calculate_sunrise_sunset,
    latlong_to_locator,
)


logger = getLogger(__name__)
call_info = Callinfo(LookupLib(lookuptype="countryfile"))

def compute_band(df: pd.DataFrame) -> pd.DataFrame:
    """Compute band for each QSO based on the frequency

    Args:
        df (pd.DataFrame): Raw data frame

    Returns:
        pd.DataFrame: Raw data frame with the new columns
    """
    logger.info("Compute band")
    df["band"] = -1
    df["band_id"] = -1
    for i, (band, freqs) in enumerate(BANDMAP.items()):
        df["band"] = np.where(
            (df["frequency"] >= freqs[0]) & (df["frequency"] <= freqs[1]),
            band,
            df["band"]
        )
        df["band_id"] = np.where(
            (df["frequency"] >= freqs[0]) & (df["frequency"] <= freqs[1]),
            i,
            df["band_id"]
        )
    return df.astype({"band": "int", "band_id": "int"})


def add_dxcc_info(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Add DXCC info")
    mylocator = latlong_to_locator(**call_info.get_lat_long(df["mycall"].values[0]))
    df = (
        df
        .join(
            pd.json_normalize(
                df.apply(
                    lambda x: call_info.get_all(x["call"]), 
                    axis=1
                )
            )
        )
        .assign(
            locator=lambda _df: _df.apply(
                lambda x: latlong_to_locator(
                    **call_info.get_lat_long(x["call"])
                ), axis=1
            ),
            distance=lambda _df: _df.apply(
                lambda x: calculate_distance(mylocator, x["locator"]), axis=1
            ),
            distance_lp=lambda _df: _df.apply(
                lambda x: calculate_distance_longpath(mylocator, x["locator"]), axis=1
            ),
            heading=lambda _df: _df.apply(
                lambda x: calculate_heading(mylocator, x["locator"]), axis=1
            ),
            heading_lp=lambda _df: _df.apply(
                lambda x: calculate_heading_longpath(mylocator, x["locator"]), axis=1
            ),
        )
    )

    df = (
        df
        .join(
            pd.json_normalize(
                df.apply(
                    lambda x: calculate_sunrise_sunset(
                        x["locator"],
                        x["datetime"].to_pydatetime()
                    ), 
                    axis=1
                )
            ),
        )
        
    )
    return df


def hour_of_contest(df: pd.DataFrame) -> pd.DataFrame:
    datetime_min = df["datetime"].min().date()
    start_utc = (
        datetime_min 
        - timedelta(days=datetime_min.weekday()) 
        + timedelta(days=5)
    )
    df = (
        df
        .assign(
            hour=(
                lambda x: (x["datetime"] - pd.to_datetime(start_utc)) 
                / pd.Timedelta("1 hour")
            )
        )
    )
    return df
