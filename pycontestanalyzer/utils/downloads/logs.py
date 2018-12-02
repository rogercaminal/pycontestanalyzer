import logging
from urllib.request import urlopen
#from urllib2 import urlopen
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def get_log(contest, callsign, year, mode):
    isgood = False
    try:
        response = None
        website_address = ""
        if contest == "cqww":
            logging.info('Getting the log from http://www.cqww.com/publiclogs/{}{}/{}.log'.format(year, mode, callsign.lower()))
            website_address = "http://www.cqww.com/publiclogs/{}{}/{}.log".format(year, mode, callsign.lower())
        elif contest == "cqwpx":
            logging.info('Getting the log from http://www.cqwpx.com/publiclogs/{}{}/{}.log'.format(year, mode, callsign.lower()))
            website_address = "http://www.cqwpx.com/publiclogs/{}{}/{}.log".format(year, mode, callsign.lower())

        with urlopen(website_address) as response:
            html = response.read()
        isgood = True
        return isgood, html
    except:
        return isgood, str("")


def get_list_of_logs(contest_type, year, mode):
    website_address = ""
    if contest_type == "cqww":
        website_address = "http://www.cqww.com/publiclogs/{}{}/".format(year, mode)
    elif contest_type == "cqwpx":
        website_address = "http://www.cqwpx.com/publiclogs/{}{}/".format(year, mode, )

    with urlopen(website_address) as response:
        html = str(response.read().decode('utf-8'))

    html = html[html.find("Number of logs found"):]
    calls = []
    for l in html.split("<"):
        if "a href=" in l:
            calls.append(l.split(">")[-1])
    del calls[calls.index("World Wide Radio Operators Foundation")]

    calls.sort()
    return calls


def get_list_of_years(contest_type):
    try:
        website_address = ""
        if contest_type == "cqww":
            website_address = "http://www.cqww.com/publiclogs/"
        elif contest_type == "cqwpx":
            website_address = "http://www.cqwpx.com/publiclogs/"

        with urlopen(website_address) as response:
            html = response.read().decode('utf-8')

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