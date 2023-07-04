"""Download module settings class definition."""

from pycontestanalyzer.config.base import BaseSettings


class DownloadSettings(BaseSettings):
    """Broadcast Reduction Settings model."""

    path_raw: str

    class Config:
        """Pydantic model config."""

        env_prefix = "PYCA_DOWNLOAD__"
