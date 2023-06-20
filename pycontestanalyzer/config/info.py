"""Settings Info class definition."""
from pycontestanalyzer.config.base import BaseSettings


class SettingsInfo(BaseSettings):
    """Settings Info model."""

    environment: str
    force_environment: str
