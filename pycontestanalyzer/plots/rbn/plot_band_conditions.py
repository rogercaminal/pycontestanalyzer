"""Plot QSO rate."""

import plotly.graph_objects as go
import plotly.offline as pyo
from pandas import Grouper
from plotly.subplots import make_subplots

from pycontestanalyzer.plots.plot_rbn_base import PlotReverseBeaconBase
from pycontestanalyzer.utils import BANDMAP


class PlotBandConditions(PlotReverseBeaconBase):
    """Plot band conditions."""

    def __init__(
        self,
        contest: str,
        mode: str,
        years: list[int],
        time_bin_size: int,
        tx_continent: str,
        rx_continents: list[str],
    ):
        """Init method of the PlotBandConditions class.

        Args:
            contest (str): Contest name
            mode (str): Mode of the contest
            years (list[int]): Years of the contest
            time_bin_size (int, optional): Time bin size in minutes.
            tx_continent (str): Continent of the TX station
            rx_continents (list[str]): Continents of the RX stations
        """
        super().__init__(contest=contest, mode=mode, years=years)
        self.time_bin_size = time_bin_size
        self.tx_continent = tx_continent
        self.rx_continents = rx_continents

    def plot(self, save: bool = False) -> None | go.Figure:
        """Create plot.

        Args:
            save (bool, optional): _description_. Defaults to False.

        Returns:
            None | Figure: _description_
        """
        grp = (
            self.data.query(f"(dx_cont == '{self.tx_continent.upper()}')")
            .query(f"(de_cont.isin({self.rx_continents}))")
            .groupby(
                [
                    "de_cont",
                    "dx_cont",
                    "band",
                    "year",
                    Grouper(key="datetime", freq=f"{self.time_bin_size}Min"),
                ],
                as_index=False,
            )
            .agg(numerator=("freq", "count"))
            .assign(
                denominator=lambda x: (
                    x.groupby(["datetime", "year"])["numerator"].transform("sum")
                ),
                ratio=lambda x: x["numerator"] / x["denominator"],
            )
        )

        bands = list(BANDMAP.keys())
        fig = make_subplots(
            rows=3,
            cols=2,
            subplot_titles=[
                f"TX continent: {self.tx_continent} - Band: {b}m" for b in bands
            ],
        )
        for i, band in enumerate(bands):
            _df = grp.query(f"band == {band}")
            fig.add_trace(
                go.Heatmap(
                    x=_df["datetime"],
                    y=_df["de_cont"],
                    z=_df["ratio"],
                    zmin=0,
                    zmax=grp["ratio"].max(),
                    name=f"{band}m",
                    hovertemplate="Date: %{x} <br>"
                    "Continent: %{y} <br>Rate of spots: %{z}",
                ),
                row=(i // 2) + 1,
                col=(i % 2) + 1,
            )

        fig.update_layout(
            hovermode="closest",
        )
        fig.update_yaxes(title="RX continent")

        if not save:
            return fig
        pyo.plot(fig, filename="band_conditions.html")
