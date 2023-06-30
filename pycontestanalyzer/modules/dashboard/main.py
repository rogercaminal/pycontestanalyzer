"""PyContestAnalyzer dashboard."""
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

# from pycontestanalyzer.modules.dashboard.layout import get_layout
from pycontestanalyzer.modules.download.main import main as _main_download


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
        if year_callsigns is None:
            return ""
        for year_callsign in year_callsigns:
            year = int(year_callsign.split(",")[0])
            callsign = year_callsign.split(",")[1]
            _main_download(
                contest=contest, years=[year], callsigns=[callsign], mode=mode
            )
        return "Downloaded!"

    app.run(debug=debug, host="0.0.0.0", port=8050)
