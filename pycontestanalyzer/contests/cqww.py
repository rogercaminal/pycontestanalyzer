from typing import Optional

from pycontestanalyzer.base.contest_base import ContestBase
from pycontestanalyzer.tasks.io.read_log_webpage import ReadLogWebpage
from pycontestanalyzer.tasks.dataframe.compute_band import ComputeBand
from pycontestanalyzer.tasks.dataframe.compute_contest_hour import ComputeContestHour


class CQWWContest(ContestBase):
    """
    Class for CQ WW contest
    """

    def __init__(
        self,
        callsign: str,
        mode: str,
        year: int,
        output_folder: Optional[str] = None,
    ):
        super().__init__(
            callsign=callsign,
            mode=mode,
            year=year,
            output_folder=output_folder,
        )

    def execute(self):
        self.task_manager.clear_kept_datasets()
        self.task_manager.clear()
        self.task_manager.add_task(
            ReadLogWebpage(
                year=self.year, mode=self.mode, callsign=self.callsign
            )
        )
        self.task_manager.add_task(
            ComputeBand(
                name="band", 
                col_frequency="freq"),
        )
        self.task_manager.add_task(
            ComputeBand(
                name="band_int", 
                col_frequency="freq", 
                band_id=True),
        )
        self.task_manager.add_task(
            ComputeContestHour(
                name="contest_hour",
                col_datetime="datetime"
            )
        )
        self.task_manager.execute()
