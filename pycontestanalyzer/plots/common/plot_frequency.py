"""Plot QSO rate."""

import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.subplots import make_subplots

from pycontestanalyzer.plots.plot_base import PlotBase
from pycontestanalyzer.utils import BANDMAP

COLORS = {
    1: "#F28F1D",
    2: "#F6C619",
    3: "#FADD75",
    4: "#2B6045",
    5: "#5EB88A",
    6: "#9ED4B9",
}


class PlotFrequency(PlotBase):
    """Plot QSOs Hour."""

    def plot(self, save: bool = False) -> None | go.Figure:
        """Create plot.

        Args:
            save (bool, optional): _description_. Defaults to False.

        Returns:
            None | Figure: _description_
        """
        fig = make_subplots(rows=6, cols=1, shared_xaxes=True)
        fig.update_layout(
            hovermode="x",
            height=1200,
        )

        for k, (callsign, year) in enumerate(self.callsigns_years):
            for j, band in enumerate([10, 15, 20, 40, 80, 160]):
                _data = (
                    self.data.query(f"(mycall.str.lower() == '{callsign.lower()}')")
                    .query(f"(year == {year})")
                    .query(f"(band == {band})")
                    .assign(
                        callsign_year=lambda x: x["mycall"]
                        + "("
                        + x["year"].astype(str)
                        + ")"
                    )
                )
                fig.append_trace(
                    go.Scatter(
                        x=_data["hour"],
                        y=_data["frequency"],
                        mode="markers",
                        marker={"color": COLORS[k + 1]},
                        name=f"{callsign} - {year}",
                        legendgroup=f"group{k+1}",
                        showlegend=True if j == 0 else False,
                    ),
                    row=j + 1,
                    col=1,
                )
                fig.update_yaxes(
                    range=BANDMAP[band], title="Frequency", row=j + 1, col=1
                )
        fig.update_xaxes(title="Contest hour", row=6, col=1)

        if not save:
            return fig
        pyo.plot(fig, filename="frequency.html")
