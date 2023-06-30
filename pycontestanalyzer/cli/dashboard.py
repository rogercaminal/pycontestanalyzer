"""PyContestAnalyzer Dashboard CLI definition."""
from logging import getLogger

from typer import Option, Typer

from pycontestanalyzer.modules.dashboard.main import main as _main

app = Typer(name="dashboard", add_completion=False)
logger = getLogger(__name__)


@app.command()
def main(
    debug: bool = Option(False, "--debug", help="Debug the dashboard"),
) -> None:
    """Dashboard main command line interface."""
    logger.info("Starting dashboard with the following commands:" "Debug = %s", debug)

    _main(debug=debug)
