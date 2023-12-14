"""PyContestAnalyzer Command Line Interface application definition."""
from typer import Typer

from pycontestanalyzer.cli.dashboard import app as app_dashboard
from pycontestanalyzer.cli.download import app as app_download
from pycontestanalyzer.cli.plot import app as app_plot
from pycontestanalyzer.commons.logging import config_logging

app = Typer(name="pycontestanalyzer", add_completion=False)
app.add_typer(app_download)
app.add_typer(app_dashboard)
app.add_typer(app_plot)
app.callback()(config_logging)
