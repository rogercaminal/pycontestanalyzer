"""PyContestAnalyzer Command Line Interface application definition."""
from typer import Typer

from pycontestanalyzer.cli.download import app as app_download
from pycontestanalyzer.commons.logging import config_logging


app = Typer(name="pycontestanalyzer", add_completion=False)
app.add_typer(app_download)
app.callback()(config_logging)