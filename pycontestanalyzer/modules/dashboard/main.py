"""PyContestAnalyzer dashboard."""
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output, State

# from pycontestanalyzer.modules.dashboard.layout import get_layout
from pycontestanalyzer.modules.download.main import exists, main as _main_download
from pycontestanalyzer.plots.common.plot_frequency import PlotFrequency
from pycontestanalyzer.plots.common.plot_qso_direction import PlotQsoDirection
from pycontestanalyzer.plots.common.plot_qsos_hour import PlotQsosHour
from pycontestanalyzer.plots.common.plot_rate import PlotRate
from pycontestanalyzer.plots.common.plot_rolling_rate import PlotRollingRate
from pycontestanalyzer.utils import CONTINENTS
from pycontestanalyzer.utils.downloads.logs import get_all_options

YEAR_MIN = 2020


def main(debug: bool = False) -> None:  # noqa: PLR0915
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
                ],
                value=None,
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
                value=None,
            )
        ],
        style={"width": "25%", "display": "inline-block"},
    )

    dropdown_year_call = html.Div(
        dcc.Dropdown(
            id="callsigns_years",
            options=[],
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
            html.Div(
                [
                    html.Div(
                        dcc.Checklist(
                            id="cl_qsos_hour_continent",
                            options=CONTINENTS,
                            value=CONTINENTS,
                            inline=True,
                        )
                    ),
                    html.Div(dcc.Graph(id="qsos_hour", figure=go.Figure())),
                ]
            ),
            html.Div(dcc.Graph(id="frequency", figure=go.Figure())),
            html.Div(
                [
                    html.Div(
                        dcc.RadioItems(
                            id="rb_qso_rate_time_bin",
                            options=[5, 15, 30, 60],
                            value=60,
                            inline=True,
                        )
                    ),
                    html.Div(dcc.Graph(id="qso_rate", figure=go.Figure())),
                ]
            ),
            html.Div(
                [
                    html.Div(
                        dcc.RadioItems(
                            id="rb_qso_rolling_rate_time_bin",
                            options=[5, 15, 30, 60],
                            value=60,
                            inline=True,
                        )
                    ),
                    html.Div(dcc.Graph(id="qso_rolling_rate", figure=go.Figure())),
                ]
            ),
            html.Div(
                [
                    html.Div(
                        dcc.RangeSlider(
                            0, 48, id="range_hour_qso_direction", value=[0, 48]
                        )
                    ),
                    html.Div(dcc.Graph(id="qso_direction", figure=go.Figure())),
                ]
            ),
        ]
    )

    @app.callback(
        Output("callsigns_years", "options"),
        [Input("contest", "value"), Input("mode", "value")],
    )
    def load_available_calls_years(contest, mode):
        if not contest or not mode:
            return []
        data = get_all_options(contest=contest.lower()).query(f"(mode == '{mode}')")
        options = [
            {"label": f"{y} - {c}", "value": f"{c},{y}"}
            for y, c in data[["year", "callsign"]].to_numpy()
        ]
        return options

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
        [Input("submit-button", "n_clicks"), Input("cl_qsos_hour_continent", "value")],
        [
            State("contest", "value"),
            State("mode", "value"),
            State("callsigns_years", "value"),
        ],
    )
    def plot_qsos_hour(n_clicks, continents, contest, mode, callsigns_years):
        f_callsigns_years = []
        if n_clicks > 0:
            for callsign_year in callsigns_years:
                callsign = callsign_year.split(",")[0]
                year = int(callsign_year.split(",")[1])
                f_callsigns_years.append((callsign, year))
                if not exists(callsign=callsign, year=year, contest=contest, mode=mode):
                    raise dash.exceptions.PreventUpdate
            return PlotQsosHour(
                contest=contest,
                mode=mode,
                callsigns_years=f_callsigns_years,
                continents=continents,
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

    @app.callback(
        Output("qso_rate", "figure"),
        [Input("submit-button", "n_clicks"), Input("rb_qso_rate_time_bin", "value")],
        [
            State("contest", "value"),
            State("mode", "value"),
            State("callsigns_years", "value"),
        ],
    )
    def plot_qso_rate(n_clicks, time_bin, contest, mode, callsigns_years):
        f_callsigns_years = []
        if n_clicks > 0:
            for callsign_year in callsigns_years:
                callsign = callsign_year.split(",")[0]
                year = int(callsign_year.split(",")[1])
                f_callsigns_years.append((callsign, year))
                if not exists(callsign=callsign, year=year, contest=contest, mode=mode):
                    raise dash.exceptions.PreventUpdate
            return PlotRate(
                contest=contest,
                mode=mode,
                callsigns_years=f_callsigns_years,
                time_bin_size=time_bin,
            ).plot()
        return go.Figure()

    @app.callback(
        Output("qso_rolling_rate", "figure"),
        [
            Input("submit-button", "n_clicks"),
            Input("rb_qso_rolling_rate_time_bin", "value"),
        ],
        [
            State("contest", "value"),
            State("mode", "value"),
            State("callsigns_years", "value"),
        ],
    )
    def plot_qso_rolling_rate(n_clicks, time_bin, contest, mode, callsigns_years):
        f_callsigns_years = []
        if n_clicks > 0:
            for callsign_year in callsigns_years:
                callsign = callsign_year.split(",")[0]
                year = int(callsign_year.split(",")[1])
                f_callsigns_years.append((callsign, year))
                if not exists(callsign=callsign, year=year, contest=contest, mode=mode):
                    raise dash.exceptions.PreventUpdate
            return PlotRollingRate(
                contest=contest,
                mode=mode,
                callsigns_years=f_callsigns_years,
                time_bin_size=time_bin,
            ).plot()
        return go.Figure()

    @app.callback(
        Output("qso_direction", "figure"),
        [
            Input("submit-button", "n_clicks"),
            Input("range_hour_qso_direction", "value"),
        ],
        [
            State("contest", "value"),
            State("mode", "value"),
            State("callsigns_years", "value"),
        ],
    )
    def plot_qso_direction(n_clicks, contest_hours, contest, mode, callsigns_years):
        f_callsigns_years = []
        if n_clicks > 0:
            for callsign_year in callsigns_years:
                callsign = callsign_year.split(",")[0]
                year = int(callsign_year.split(",")[1])
                f_callsigns_years.append((callsign, year))
                if not exists(callsign=callsign, year=year, contest=contest, mode=mode):
                    raise dash.exceptions.PreventUpdate
            return PlotQsoDirection(
                contest=contest,
                mode=mode,
                callsigns_years=f_callsigns_years,
                contest_hours=contest_hours,
            ).plot()
        return go.Figure()

    app.run(debug=debug, host="0.0.0.0", port=8050)
