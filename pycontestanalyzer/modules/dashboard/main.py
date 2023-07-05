"""PyContestAnalyzer dashboard."""
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output, State

# from pycontestanalyzer.modules.dashboard.layout import get_layout
from pycontestanalyzer.modules.download.main import main as _main_download
from pycontestanalyzer.plots.common.plot_qsos_hour import PlotQsosHour

N_CLICKS = 0


def main(debug: bool = False) -> None:
    """Main dashboard entrypoint.

    This method generates the dashboard to be displayed with the analysis of each
    contest.

    Args:
        debug: boolean with the debug option of dash
    """
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # app.layout = get_layout()
    app.layout = html.Div(
        [
            html.Div(
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
            ),
            html.Div(
                [
                    dcc.RadioItems(
                        id="mode",
                        options=[
                            {"label": "CW", "value": "cw"},
                            {"label": "SSB", "value": "ssb"},
                            {"label": "MIXED", "value": "mixed"},
                        ],
                        value="cw",
                    )
                ],
                style={"width": "25%", "display": "inline-block"},
            ),
            html.Div(
                dcc.Dropdown(
                    id="year_callsigns",
                    options=[
                        {"label": "2021 - EA6FO", "value": "2021,EA6FO"},
                        {"label": "2022 - EF6T", "value": "2022,EF6T"},
                    ],
                    multi=True,
                ),
                style={"width": "25%", "display": "inline-block"},
            ),
            html.Div(
                html.Button(
                    id="submit-button",
                    n_clicks=0,
                    children="submit",
                    style={"fontsize": 24},
                )
            ),
            html.Div(id="printout_arguments"),
            html.Div(dcc.Graph(id="qsos_hour")),
        ]
    )

    @app.callback(
        Output("printout_arguments", "children"),
        [Input("submit-button", "n_clicks")],
        [
            State("contest", "value"),
            State("mode", "value"),
            State("year_callsigns", "value"),
        ],
    )
    def run_download(n_clicks, contest, mode, year_callsigns):
        # if year_callsigns is None:
        if n_clicks <= N_CLICKS:
            return ""
        for year_callsign in year_callsigns:
            year = int(year_callsign.split(",")[0])
            callsign = year_callsign.split(",")[1]
            _main_download(
                contest=contest, years=[year], callsigns=[callsign], mode=mode
            )
        return "Downloaded!"

    @app.callback(
        Output("qsos_hour", "figure"),
        [Input("printout_arguments", "children")],
        [
            State("contest", "value"),
            State("mode", "value"),
            State("year_callsigns", "value"),
        ],
    )
    def plot_qsos_hour(printout_text, contest, mode, year_callsigns):
        if printout_text != "Downloaded!":
            return go.Figure()
        callsigns = []
        years = []
        for year_callsign in year_callsigns:
            years.append(int(year_callsign.split(",")[0]))
            callsigns.append(year_callsign.split(",")[1])
        return PlotQsosHour(
            callsigns=callsigns, contest=contest, mode=mode, years=years
        ).plot()

    app.run(debug=debug, host="0.0.0.0", port=8050)
