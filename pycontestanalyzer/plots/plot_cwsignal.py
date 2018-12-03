from pycontestanalyzer.plots.plot_base import PlotBase
import plotly.offline as py
import plotly.graph_objs as go


class PlotCWSignal(PlotBase):

    def __init__(self, name):
        super(PlotCWSignal, self).__init__(name)

    def do_plot(self, contest, doSave, options=""):

        extra_conditions = (contest.rbspots["speed"] > 0.)
        for opt in options.split(","):
            if "callsign" in opt:
                callsign = opt.replace("callsign", "")
                extra_conditions &= (contest.rbspots["callsign"] == str("{}".format(callsign)))
            if "band" in opt:
                band = opt.replace("band", "")
                extra_conditions &= (contest.rbspots["band"] == str("%sm" % band))

        # Define the datasets
        y = contest.rbspots[extra_conditions].groupby("date")["db"].mean()
        x = y.index.tolist()
        data = [
                go.Scatter(x=x, y=y, line=dict(color='blue',   width=4), hoverinfo="x+y", mode="lines", name="CW speed"),
                ]

        title = 'Signal strength vs date'
        if "band" in options:
            title += str(" {}m".format(options.replace("band", "")))
        if "callsign" in options:
            title += str(" de {}".format(options.replace("callsign", "")))

        layout = go.Layout(
            barmode='stack',
            title=title,
            xaxis=dict(title="Time", rangeselector=dict(buttons=[dict(count=1, label='1h', step='hour', stepmode='backward'), dict(count=6, label='6h', step='hour', stepmode='backward'), dict(count=12, label='12h', step='hour', stepmode='backward'), dict(count=24, label='24h', step='hour', stepmode='backward'), dict(step='all')]), rangeslider=dict()),
            yaxis=dict(title="Signal strength [dB]"),
            width=750,
            height=750,
        )

        fig = go.Figure(data=data, layout=layout)
        return py.plot(fig, auto_open=False, output_type='div')