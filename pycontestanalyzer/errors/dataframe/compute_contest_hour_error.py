from typing import Optional
from pycontestanalyzer.base.error_base import ErrorBase


class ComputeContestHourError(ErrorBase):
    """Base exception for properties of ComputeContestHour"""

    def __init__(self, message: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)