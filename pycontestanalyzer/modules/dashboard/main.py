import dash
import dash_core_components as dcc
import dash_html_components as html

def main():
    app = dash.Dash()

    app.layout = html.Div(
        [
            html.Label("Hello world!")
        ]
    )

    app.run()