from typing import Optional


class ErrorBase(Exception):
    """Base exception for pycontestanalyzer"""

    def __init__(self, message: Optional[str] = None, **kwargs):
        super().__init__(message)
        # Store kwargs for specific uses in derived class errors
        self.kwargs = kwargs
