"""Download the data from the server"""
import logging

from pycontestanalyzer.config import get_settings
from pycontestanalyzer.data.online_cqww_cabrillo import OnlineCQWWCabrilloDataSource

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
    
    reader = OnlineCQWWCabrilloDataSource(callsign="EF6T", year=2022, mode="cw")
    df = reader.load()


    settings = get_settings()

    # logger.info("Training data from date %s to %s", start_date, end_date)
    # logger.info("Forecasting data from date %s", forecast_start_date)

    # s3_prefix_performance = settings.s3.paths.performance.format(
    #     isoyear=isoyear,
    #     isoweek=isoweek,
    #     country=country,
    # )
    # s3_prefix_temporary = settings.s3.paths.temporary

    # # --- Data input
    # # get dataframe with relation of catchment areas to pools.
    # logger.info("Loading input data.")
    # catchment_areas = CatchmentAreasDataSource(connection=connection).load()

    # sr_data = CombinedSuccessRateDataSource(
    #     connection=connection,
    #     start_date=start_date.date(),
    #     end_date=end_date.date(),
    #     zones=zones,
    # ).load()

    # sr_data = merge_dataframes(
    #     left=sr_data, right=catchment_areas, how="left", on=["stuart_delivery_area"]
    # )

    # geo_level_granularities = list(settings.performance.models.keys())
    # logger.info("Loaded input data.")
    # # --- END Data input

    # performance_output_storage_sink = PerformanceOutputStorageSink(
    #     prefix=s3_prefix_performance,
    # )
    # performance_output_databse_sink = PerformanceOutputDatabaseSink(
    #     connection=connection,
    #     iam_role=settings.redshift.s3_iam_role,
    #     prefix=s3_prefix_temporary,
    # )

    # for geo_level_granularity in geo_level_granularities:
    #     # --- Data manipulation
    #     logger.info(
    #         f"Data manipulation for geo_level_granularity: {geo_level_granularity}"
    #     )
    #     df_fe = data_manipulation(
    #         df=sr_data,
    #         frequency=settings.performance.time_frequency,
    #         geo_level_granularity=geo_level_granularity,
    #     )
    #     # --- END Data manipulation