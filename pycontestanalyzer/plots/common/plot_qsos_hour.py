"""Plot QSO rate."""

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
from pandas import DataFrame

from pycontestanalyzer.plots.plot_base import PlotBase

COLORS = {
    10: "#F28F1D",
    15: "#F6C619",
    20: "#FADD75",
    40: "#2B6045",
    80: "#5EB88A",
    160: "#9ED4B9",
}


class PlotQsosHour(PlotBase):
    """Plot QSOs Hour."""

    def plot(self, save: bool = False) -> None | go.Figure:
        """Create plot.

        Args:
            save (bool, optional): _description_. Defaults to False.

        Returns:
            None | Figure: _description_
        """
        # Groupby data
        grp = (
            self.data.assign(hour_rounded=lambda x: np.floor(x["hour"]))
            .groupby(
                ["mycall", "year", "band", "band_id", "hour_rounded"], as_index=False
            )
            .aggregate(qsos=("call", "count"))
        )

        grp = (
            DataFrame(np.arange(0, 48, 1), columns=["hour_rounded"])
            .merge(
                DataFrame(
                    grp[["mycall", "year"]].drop_duplicates(),
                    columns=["mycall", "year"],
                ),
                how="cross",
            )
            .merge(grp[["band", "band_id"]].drop_duplicates(), how="cross")
            .merge(
                grp,
                how="left",
                on=["hour_rounded", "mycall", "year", "band", "band_id"],
            )
            .fillna(0)
            .astype({"qsos": int, "band": str})
            .merge(
                (
                    grp.groupby(
                        ["mycall", "year", "hour_rounded"], as_index=False
                    ).aggregate(total_qsos=("qsos", "sum"))
                ),
                how="left",
                on=["mycall", "year", "hour_rounded"],
            )
            .fillna(0)
            .assign(
                callsign_year=lambda x: x["mycall"] + "(" + x["year"].astype(str) + ")",
            )
        )

        fig = px.bar(
            grp,
            x="hour_rounded",
            y="qsos",
            custom_data=["total_qsos"],
            color="band",
            facet_row="callsign_year",
            labels={
                "callsign_year": "Callsign (year)",
                "hour_rounded": "Contest hour",
                "qsos": "QSOs",
                "band": "Band",
            },
        )
        fig.update_layout(hovermode="x unified")
        fig.update_xaxes(title="Contest hour")
        fig.update_yaxes(title="QSOs")

        if not save:
            return fig
        pyo.plot(fig, filename="qsos_hour.html")
