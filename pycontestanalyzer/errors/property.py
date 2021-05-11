from typing import Optional
from pycontestanalyzer.base.error_base import ErrorBase


class PropertyError(ErrorBase):
    """Base exception for properties of pycontestanalyzer"""

    def __init__(self, message: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)


class PropertyGetterError(PropertyError):
    """Base exception for property getters of pycontestanalyzer"""

    def __init__(self, message: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)


class PropertySetterError(PropertyError):
    """Base exception for property setters of pycontestanalyzer"""

    def __init__(self, message: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
