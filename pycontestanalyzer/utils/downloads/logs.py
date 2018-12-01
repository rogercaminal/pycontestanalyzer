import logging
#from urllib.request import urlopen
from urllib2 import urlopen


def get_log(contestType, callsign, year, mode):
    isgood = False
    try:
        response = None
        if contestType=="cqww":
            logging.info('Getting the log from http://www.cqww.com/publiclogs/%s%s/%s.log'%(year, mode, callsign.lower()))
            response = urlopen("http://www.cqww.com/publiclogs/%s%s/%s.log"%(year, mode, callsign.lower()))
        elif contestType=="cqwpx":
            logging.info('Getting the log from http://www.cqwpx.com/publiclogs/%s%s/%s.log'%(year, mode, callsign.lower()))
            response = urlopen("http://www.cqwpx.com/publiclogs/%s%s/%s.log"%(year, mode, callsign.lower()))
        html = response.read()
        isgood = True
        return isgood, html
    except:
        return isgood, str("")


def get_list_of_logs(contestType, year, mode):
    response = None
    if contestType=="cqww":
        response = urlopen("http://www.cqww.com/publiclogs/%s%s/"%(year, mode))
    elif contestType=="cqwpx":
        response = urlopen("http://www.cqwpx.com/publiclogs/%s%s/"%(year, mode, ))
    html = str(response.read())

    html = html[html.find("Number of logs found"):]
    calls = []
    for l in html.split("<"):
        if "a href=" in l:
            calls.append(l.split(">")[-1])
    del calls[calls.index("World Wide Radio Operators Foundation")]

    calls.sort()
    return calls


def get_list_of_years(contestType):
    try:
        response = None
        if contestType=="cqww":
            response = urlopen("http://www.cqww.com/publiclogs/")
        elif contestType=="cqwpx":
            response = urlopen("http://www.cqwpx.com/publiclogs/")
        html = str(response.read())

        years = []
        for l in html.split("\n"):
            if "View CQ W" in l:
                year = l.split()[5]
                if year not in years:
                    years.append(year)

        years.sort()
        return years
    except:
        return ["2016"]