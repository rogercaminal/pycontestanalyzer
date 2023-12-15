"""PyContestAnalyzer dashboard."""
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State

from pycontestanalyzer.modules.download.main import (
    exists_rbn,
    download_rbn_data,
)
from pycontestanalyzer.plots.rbn.plot_snr_band_continent import PlotSnrBandContinent
from pycontestanalyzer.utils import CONTINENTS

YEAR_MIN = 2020


def main(debug: bool = False) -> None:  # noqa: PLR0915
    """Main dashboard entrypoint.

    This method generates the dashboard to be displayed with the analysis of each
    contest.

    Args:
        debug: boolean with the debug option of dash
    """
    app = dash.Dash(
        __name__, 
        external_stylesheets=[dbc.themes.BOOTSTRAP], 
        prevent_initial_callbacks=True
    )

    # Buttons
    radio_contest = html.Div(
        [
            dcc.RadioItems(
                id="contest",
                options=[
                    {"label": "CQ WW DX", "value": "cqww"},
                    {"label": "CQ WPX", "value": "cqwpx"},
                    {"label": "IARU", "value": "iaru"},
                ],
                value=None,
            )
        ],
        style={"width": "25%", "display": "inline-block"},
    )

    input_year = html.Div(
        dcc.Input(
            id="year",
            placeholder="Enter year of the contest...",
            type="number",
            value="",
        ),
        style={"width": "25%", "display": "inline-block"},
    )

    input_call = html.Div(
        dcc.Input(
            id="callsigns",
            placeholder="Enter a comma-separated list of calls...",
            type="text",
            value='',
        ),
        style={"width": "25%", "display": "inline-block"},
    )

    dropdown_bands = html.Div(
        dcc.Dropdown(
            id="bands",
            options=[10, 15, 20, 40, 80, 160],
            multi=True,
            value=[10, 15, 20, 40, 80, 160],
        ),
        style={"width": "25%", "display": "inline-block"},
    )
    dropdown_time_bin_size = html.Div(
        dcc.Dropdown(
            id="time_bin_size",
            options=[5, 10, 30, 60],
            multi=False,
            value=10,
        ),
        style={"width": "25%", "display": "inline-block"},
    )
    dropdown_continents = html.Div(
        dcc.Dropdown(
            id="rx_continents",
            options=CONTINENTS,
            multi=True,
            value=["AS", "EU", "NA"],
        ),
        style={"width": "25%", "display": "inline-block"},
    )

    app.layout = html.Div(
        [
            radio_contest,
            input_year,
            input_call,
            dropdown_bands,
            dropdown_time_bin_size,
            dropdown_continents,
            html.Div(
                html.Button(
                    id="submit-button",
                    n_clicks=0,
                    children="submit",
                    style={"fontsize": 24},
                )
            ),
            html.Div(
                dcc.Graph(
                    id="snr_plot", 
                    figure=go.Figure(), 
                    responsive=True,
                    style={"flex": 1, "min-width": 700}
                )
            ),
            dcc.Store(id="signal"),
        ]
    )

    @app.callback(
        Output("signal", "data"),
        [Input("submit-button", "n_clicks")],
        [
            State("contest", "value"),
            State("year", "value"),
        ],
    )
    def run_download(n_clicks, contest, year):
        if n_clicks > 0:
            if not exists_rbn(contest=contest, year=year, mode="cw"):
                pass
                download_rbn_data(contest=contest, years=[year], mode="cw")
        return True
    

    @app.callback(
        Output("snr_plot", "figure"),
        [Input("signal", "data")],
        [
            State("contest", "value"),
            State("callsigns", "value"),
            State("year", "value"),
            State("bands", "value"),
            State("time_bin_size", "value"),
            State("rx_continents", "value"),
        ],
    )
    def plot_snr(signal, contest, callsigns, year, bands, time_bin_size, rx_continents):
        if not signal:
            raise dash.exceptions.PreventUpdate
        calls = callsigns.strip().split(",")
        return PlotSnrBandContinent(
            contest=contest, 
            callsigns=calls, 
            mode="cw", 
            bands=bands, 
            year=int(year), 
            time_bin_size=time_bin_size, 
            rx_continents=rx_continents
        ).plot()
    
    app.run(debug=debug, host="0.0.0.0", port=8050)
