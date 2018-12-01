import pickle
import logging

logging.basicConfig(format='%(levelname)s: %(asctime)s UTC  -  contest.py : %(message)s', level=logging.DEBUG)


def retrieve_contest_object(search_info):
    contestType = search_info["name"]
    callsign = search_info["callsign"]
    year = search_info["year"]
    mode = search_info["mode"]

    logname = "ContestAnalyzerOnline/contestAnalyzer/data/%s_%s_%s_%s/log_%s_%s_%s_%s.log" % (contestType, year, mode, callsign, contestType, year, mode, callsign)

    contest = None
    with open("%s.pickle" % logname.replace(".log", ""), 'rb') as myinput:
        contest = pickle.load(myinput)
    return contest