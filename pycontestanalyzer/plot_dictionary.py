from pycontestanalyzer.plot_manager import PlotManager
from pycontestanalyzer.plots.plot_qsos_vs_time__band import PlotQSOsVsTimeBand
from pycontestanalyzer.plots.plot_qsos_vs_time__continent import PlotQSOsVsTimeContinent
from pycontestanalyzer.plots.plot_qsos_vs_time__stationtype import PlotQSOsVsTimeStationtype
from pycontestanalyzer.plots.plot_fraction_stationtype import PlotFractionStationtype
from pycontestanalyzer.plots.plot_ratio_qsos_min import PlotRatioQSOsMin
from pycontestanalyzer.plots.plot_mults_vs_qsos import PlotMultsVsQSOs
from pycontestanalyzer.plots.plot_time_vs_band_vs_continent import PlotTimeVsBandVsContinent
from pycontestanalyzer.plots.plot_freq_vs_date import PlotFreqVsDate
from pycontestanalyzer.plots.plot_lenghtcallmorse import PlotLenghtCallMorse
from pycontestanalyzer.plots.plot_heading import PlotHeading
from pycontestanalyzer.plots.plot_db_vs_date import PlotDbVsDate
from pycontestanalyzer.plots.plot_cwspeed import PlotCWSpeed

plot_dictionary = PlotManager()

plot_dictionary.add_plot("plot_qsos_vs_time__band", PlotQSOsVsTimeBand("plot_qsos_vs_time__band"))
plot_dictionary.add_plot("plot_qsos_vs_time__continent", PlotQSOsVsTimeContinent("plot_qsos_vs_time__continent"))
plot_dictionary.add_plot("plot_qsos_vs_time__stationtype", PlotQSOsVsTimeStationtype("plot_qsos_vs_time__stationtype"))
plot_dictionary.add_plot("plot_fraction_stationtype", PlotFractionStationtype("plot_fraction_stationtype"))
plot_dictionary.add_plot("plot_ratio_qsos_min", PlotRatioQSOsMin("plot_ratio_qsos_min"))
plot_dictionary.add_plot("plot_mults_vs_qsos", PlotMultsVsQSOs("plot_mults_vs_qsos"))
plot_dictionary.add_plot("plot_time_vs_band_vs_continent", PlotTimeVsBandVsContinent("plot_time_vs_band_vs_continent"))
plot_dictionary.add_plot("plot_freq_vs_date", PlotFreqVsDate("plot_freq_vs_date"))
plot_dictionary.add_plot("plot_lenghtcallmorse", PlotLenghtCallMorse("plot_lenghtcallmorse"))
plot_dictionary.add_plot("plot_heading", PlotHeading("plot_heading"))
plot_dictionary.add_plot("plot_db_vs_date", PlotDbVsDate("plot_db_vs_date"))
plot_dictionary.add_plot("plot_cwspeed", PlotCWSpeed("plot_cwspeed"))
