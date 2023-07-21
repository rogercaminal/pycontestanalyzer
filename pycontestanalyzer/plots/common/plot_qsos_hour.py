"""Plot QSO rate."""

import numpy as np
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
            .astype({"qsos": int})
            .merge(
                (
                    grp.groupby(
                        ["mycall", "year", "hour_rounded"], as_index=False
                    ).aggregate(total_qsos=("qsos", "sum"))
                ),
                how="left",
                on=["mycall", "year", "hour_rounded"],
            )
        )

        # Create figure and layout
        layout = go.Layout(
            title="QSOs / hour",
            xaxis={"title": "Contest hour"},
            yaxis={"title": "# QSOs"},
            yaxis2=go.layout.YAxis(
                visible=False,
                matches="y",
                overlaying="y",
                anchor="x",
            ),
            barmode="stack",
            showlegend=True,
            hovermode="closest",
            yaxis_range=[0, grp["total_qsos"].max() * 1.1],
        )
        fig = go.Figure(layout=layout)

        # Create bar plot
        offset_ratio = 1 / (len(grp[["mycall", "year"]].drop_duplicates()) + 1)
        rows = (
            grp[["year", "mycall"]].drop_duplicates().reset_index(drop=True).iterrows()
        )
        for i, row in rows:
            year = row["year"]
            mycall = row["mycall"]
            for band in grp["band"].unique():
                dff = grp.query(
                    f"(year == {year}) & (mycall == '{mycall}') & (band == {band})"
                )
                fig.add_bar(
                    x=dff["hour_rounded"],
                    y=dff["qsos"],
                    customdata=dff[["band", "mycall", "total_qsos", "year"]],
                    yaxis=f"y{i+1}",
                    offsetgroup=str(i),
                    offset=(i - 1) * offset_ratio,
                    width=offset_ratio,
                    showlegend=True if i == 0 else False,
                    legendgroup=mycall,
                    legendgrouptitle_text="bands",
                    name=f"{band}m",
                    marker_color=COLORS[band],
                    marker_line=dict(width=2, color="#333"),
                    hovertemplate="<b>%{customdata[1]} (%{customdata[3]}) \
                        <br>hour:%{x}</b><br>QSOs %{customdata[0]}m:%{y} \
                            <br>QSOs total:%{customdata[2]}",
                )
        if not save:
            return fig
        pyo.plot(fig, filename="qsos_hour.html")
