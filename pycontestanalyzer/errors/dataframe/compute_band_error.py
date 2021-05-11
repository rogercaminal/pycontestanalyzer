from typing import Optional
from pycontestanalyzer.base.error_base import ErrorBase


class ComputeBandError(ErrorBase):
    """Base exception for properties of ComputeBand"""

    def __init__(self, message: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)