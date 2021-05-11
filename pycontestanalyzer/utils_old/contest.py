import pickle
import logging

logging.basicConfig(
    format="%(levelname)s: %(asctime)s UTC  -  contest.py : %(message)s",
    level=logging.DEBUG,
)


def retrieve_contest_object(search_info, output_folder):
    contest_type = search_info["name"]
    callsign = search_info["callsign"]
    year = search_info["year"]
    mode = search_info["mode"]

    logname = "{output_folder}/{contest_type}_{year}_{mode}_{callsign}/log_{contest_type}_{year}_{mode}_{callsign}.log".format(
        output_folder=output_folder,
        contest_type=contest_type,
        year=year,
        mode=mode,
        callsign=callsign,
    )

    contest = None
    with open("%s.pickle" % logname.replace(".log", ""), "rb") as myinput:
        contest = pickle.load(myinput)
    return contest
