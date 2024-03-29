"""Download the data from the server."""
import logging
import os

from pycontestanalyzer.config import get_settings
from pycontestanalyzer.data.cqww.storage_source import RawCQWWCabrilloDataSource
from pycontestanalyzer.data.raw_contest_sink import (
    RawCabrilloDataSink,
    RawCabrilloMetaDataSink,
)
from pycontestanalyzer.data.raw_rbn_sink import RawReverseBeaconDataSink
from pycontestanalyzer.data.rbn.storage_source import ReverseBeaconRawDataSource
from pycontestanalyzer.modules.download.data_manipulation import data_manipulation

logger = logging.getLogger(__name__)


def exists(contest: str, year: int, callsign: str, mode: str) -> bool:
    """Parquet exists for that call/contest/year/mode.

    Args:
        contest (str): string with he name of the contest (case insensitive)
        year (int): year of the contest
        callsign (str): callsign used in the contest (case insensitive)
        mode (str): mode of the contest

    Returns:
        bool: partition exists
    """
    settings = get_settings()
    path = settings.storage.paths.raw_data.format(
        contest=contest, mode=mode, year=year, callsign=callsign
    )
    return os.path.exists(path=path)


def exists_rbn(contest: str, year: int, mode: str) -> bool:
    """Parquet exists for RBN info.

    Args:
        contest (str): string with the name of the contest (case insensitive)
        year (int): year of the contest
        mode (str): mode of the contest

    Returns:
        bool: partition exists
    """
    settings = get_settings()
    path = settings.storage.paths.raw_rbn.format(contest=contest, mode=mode, year=year)
    return os.path.exists(path=path)


def main(
    contest: str, years: list[int], callsigns: list[str], mode: str, force: bool = False
) -> None:
    """Main download & data engineering entrypoint.

    This method performs the main workflow in order to download the cabrillo file(s)
    from the given website, and implement the set of features that then will be used
    in the plotting step. The resulting data set is stored locally in the path
    specified in the settings.

    Args:
        contest (str): string with the name of the contest (case insensitive).
        years (list[int]): list of integers with the years to consider.
        callsigns (list[str]): list of (case insensitive) strings containing the
            callsigns to consider.
        mode (str): mode of the contest.
        force (bool, optional): force download even if it exists. Defaults to False.
    """
    settings = get_settings()

    logger.info("Downloading data from the server")
    for callsign in callsigns:
        for year in years:
            if (
                not exists(contest=contest, year=year, mode=mode, callsign=callsign)
                or force
            ):
                logger.info(f"  - {contest} - {mode} - {year} - {callsign}")
                # Get data
                contest_data = RawCQWWCabrilloDataSource(
                    callsign=callsign, year=year, mode=mode
                ).load()

                # Feature engineering
                contest_data = data_manipulation(data=contest_data)

                # Store data
                prefix_raw_storage_data = settings.storage.paths.raw_data.format(
                    contest=contest, mode=mode, year=year, callsign=callsign.lower()
                )
                prefix_raw_storage_metadata = (
                    settings.storage.paths.raw_metadata.format(
                        contest=contest, mode=mode, year=year, callsign=callsign.lower()
                    )
                )
                logger.info(f"Store data in {prefix_raw_storage_data}")
                RawCabrilloDataSink(prefix=prefix_raw_storage_data).push(contest_data)

                logger.info(f"Store metadata in {prefix_raw_storage_metadata}")
                RawCabrilloMetaDataSink(prefix=prefix_raw_storage_metadata).push(
                    contest_data
                )
            else:
                logger.info(
                    f"\t- {contest} - {mode} - {year} - {callsign} already exists!"
                )

    logger.info("Downloading RBN for the contest")
    for year in years:
        if not exists_rbn(contest=contest, year=year, mode=mode):
            logger.info(f"  - RBN: {contest} - {mode} - {year}")
            # Load data
            rbn_data = ReverseBeaconRawDataSource(
                contest=contest, year=year, mode=mode
            ).load()
            # Store data
            prefix_raw_rbn_data = settings.storage.paths.raw_rbn.format(
                contest=contest, mode=mode, year=year
            )
            logger.info(f"Store data in {prefix_raw_rbn_data}")
            RawReverseBeaconDataSink(prefix=prefix_raw_rbn_data).push(rbn_data)
        else:
            logger.info(f"\t- RBN for {contest} - {mode} - {year} already exists!")
