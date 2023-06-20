"""Download module settings class definition."""

from pycontestanalyzer.config.base import BaseSettings


class DownloadSettings(BaseSettings):
    """Broadcast Reduction Settings model."""

    path_raw: str
