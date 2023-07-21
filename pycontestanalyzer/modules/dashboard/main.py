"""PyContestAnalyzer dashboard."""
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output, State

# from pycontestanalyzer.modules.dashboard.layout import get_layout
from pycontestanalyzer.modules.download.main import exists, main as _main_download
from pycontestanalyzer.plots.common.plot_frequency import PlotFrequency
from pycontestanalyzer.plots.common.plot_qsos_hour import PlotQsosHour


def main(debug: bool = False) -> None:
    """Main dashboard entrypoint.

    This method generates the dashboard to be displayed with the analysis of each
    contest.

    Args:
        debug: boolean with the debug option of dash
    """
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Buttons
    radio_contest = html.Div(
        [
            dcc.RadioItems(
                id="contest",
                options=[
                    {"label": "CQ WW DX", "value": "cqww"},
                    {"label": "CQ WPX", "value": "cqwpx"},
                    {"label": "IARU HF", "value": "iaruhf"},
                ],
                value="cqww",
            )
        ],
        style={"width": "25%", "display": "inline-block"},
    )

    radio_mode = html.Div(
        [
            dcc.RadioItems(
                id="mode",
                options=[
                    {"label": "CW", "value": "cw"},
                    {"label": "SSB", "value": "ssb"},
                ],
                value="cw",
            )
        ],
        style={"width": "25%", "display": "inline-block"},
    )

    dropdown_year_call = html.Div(
        dcc.Dropdown(
            id="callsigns_years",
            options=[
                {"label": "2021 - EA6FO", "value": "EA6FO,2021"},
                {"label": "2022 - EF6T", "value": "EF6T,2022"},
            ],
            multi=True,
            value=None,
        ),
        style={"width": "25%", "display": "inline-block"},
    )

    # app.layout = get_layout()
    app.layout = html.Div(
        [
            radio_contest,
            radio_mode,
            dropdown_year_call,
            html.Div(
                html.Button(
                    id="submit-button",
                    n_clicks=0,
                    children="submit",
                    style={"fontsize": 24},
                )
            ),
            html.P(id="download"),
            html.Div(dcc.Graph(id="qsos_hour", figure=go.Figure())),
            html.Div(dcc.Graph(id="frequency", figure=go.Figure())),
        ]
    )

    @app.callback(
        Output("download", "children"),
        [Input("submit-button", "n_clicks")],
        [
            State("contest", "value"),
            State("mode", "value"),
            State("callsigns_years", "value"),
        ],
    )
    def run_download(n_clicks, contest, mode, callsigns_years):
        if n_clicks > 0:
            for callsign_year in callsigns_years:
                callsign = callsign_year.split(",")[0]
                year = int(callsign_year.split(",")[1])
                if not exists(contest=contest, year=year, mode=mode, callsign=callsign):
                    _main_download(
                        contest=contest, years=[year], callsigns=[callsign], mode=mode
                    )
        return n_clicks

    @app.callback(
        Output("qsos_hour", "figure"),
        [Input("submit-button", "n_clicks")],
        [
            State("contest", "value"),
            State("mode", "value"),
            State("callsigns_years", "value"),
        ],
    )
    def plot_qsos_hour(n_clicks, contest, mode, callsigns_years):
        f_callsigns_years = []
        if n_clicks > 0:
            for callsign_year in callsigns_years:
                callsign = callsign_year.split(",")[0]
                year = int(callsign_year.split(",")[1])
                f_callsigns_years.append((callsign, year))
                if not exists(callsign=callsign, year=year, contest=contest, mode=mode):
                    raise dash.exceptions.PreventUpdate
            return PlotQsosHour(
                contest=contest, mode=mode, callsigns_years=f_callsigns_years
            ).plot()
        return go.Figure()

    @app.callback(
        Output("frequency", "figure"),
        [Input("submit-button", "n_clicks")],
        [
            State("contest", "value"),
            State("mode", "value"),
            State("callsigns_years", "value"),
        ],
    )
    def plot_frequency(n_clicks, contest, mode, callsigns_years):
        f_callsigns_years = []
        if n_clicks > 0:
            for callsign_year in callsigns_years:
                callsign = callsign_year.split(",")[0]
                year = int(callsign_year.split(",")[1])
                f_callsigns_years.append((callsign, year))
                if not exists(callsign=callsign, year=year, contest=contest, mode=mode):
                    raise dash.exceptions.PreventUpdate
            return PlotFrequency(
                contest=contest, mode=mode, callsigns_years=f_callsigns_years
            ).plot()
        return go.Figure()

    app.run(debug=debug, host="0.0.0.0", port=8050)
