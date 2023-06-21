"""Download the data from the server"""
import logging

from pycontestanalyzer.config import get_settings
from pycontestanalyzer.data.cqww.storage_source import RawCQWWCabrilloDataSource
from pycontestanalyzer.data.raw_contest_sink import (
    RawCabrilloDataSink, RawCabrilloMetaDataSink
)
from pycontestanalyzer.modules.download.data_manipulation import data_manipulation

logger = logging.getLogger(__name__)


def main (
    contest: str, 
    years: list[int], 
    callsigns: list[str], 
    mode: str
) -> None:
    """Main download & data engineering entrypoint.

    This method performs the main workflow in order to download the cabrillo file(s)
    from the given website, and implement the set of features that then will be used
    in the plotting step. The resulting data set is stored locally in the path 
    specified in the settings.

    Args:
        contest: string with the name of the contest (case insensitive).
        years: list of integers with the years to consider.
        callsigns: list of (case insensitive) strings containing the callsigns to
            consider.
        mode: string with the mode of the contest.
    """
    settings = get_settings()

    logger.info("Downloading data from the server")
    for callsign in callsigns:
        logger.info(f"- {callsign}")
        for year in years:
            logger.info(f"  - {year}")
            # Get data
            contest_data = RawCQWWCabrilloDataSource(
                callsign=callsign, 
                year=year, 
                mode=mode
            ).load()

            # Feature engineering
            contest_data = data_manipulation(data=contest_data)

            # Store data
            prefix_raw_storage_data = settings.storage.paths.raw_data.format(
                contest=contest,
                mode=mode,
                callsign=callsign
            )
            prefix_raw_storage_metadata = settings.storage.paths.raw_metadata.format(
                contest=contest,
                mode=mode,
                callsign=callsign
            )
            logger.info(f"Store data in {prefix_raw_storage_data}")
            RawCabrilloDataSink(prefix=prefix_raw_storage_data).push(contest_data)

            logger.info(f"Store metadata in {prefix_raw_storage_metadata}")
            RawCabrilloMetaDataSink(prefix=prefix_raw_storage_metadata).push(
                contest_data
            )
