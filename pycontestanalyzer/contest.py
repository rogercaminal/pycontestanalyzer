import logging
import os
import numpy as np
import pandas as pd
from pycontestanalyzer.utils.downloads.logs import get_log


class Contest(object):
    def __init__(self, contest, year, mode, callsign, output_folder, force_csv=False):
        self.callsign = callsign
        self.mode = mode
        self.year = year
        self.contest = contest
        self.output_folder = output_folder
        self.force_csv = force_csv

        self.cat_contest = ""
        self.cat_operator = ""
        self.cat_assisted = ""
        self.cat_band = ""
        self.cat_power = ""
        self.cat_transmitter = ""
        self.category = ""
        self.operator_names = ""
        self.location = ""
        self.operators = []
        self.club = ""
        self.log = None
        self.rbspots = None

        self.save = False

        self.log_path = ""
        self.log_name = ""

        self.max_rates = {}
        self.rates_per_minute = []

        self.call_exists, self.download_ok = self.import_log()

    def __str__(self):
        line = ""
        line += "Call: %s\n" % self.callsign
        line += "Contest: %s\n" % self.contest
        line += "Category operator: %s\n" % self.cat_operator
        line += "Category assisted: %s\n" % self.cat_assisted
        line += "Category band: %s\n" % self.cat_band
        line += "Category power: %s\n" % self.cat_power
        line += "Category mode: %s\n" % self.mode
        line += "Category transmitter: %s\n" % self.cat_transmitter
        line += "Operator names: %s\n" % self.operator_names
        line += "Location: %s\n" % self.location
        line += "Operator(s) call(s): %s\n" % (' '.join(self.operators))
        line += "Club: %s\n" % self.club
        return line 

    def import_log(self):
        # def import_log(contest, contestType, year, mode, callsign, forceCSV=False):
        # --- Type of initial variables
        dict_types = {}
        dict_types["frequency"] = np.float64
        dict_types["mode"] = np.object
        dict_types["date"] = np.object
        dict_types["time"] = np.object
        dict_types["mycall"] = np.object
        dict_types["urrst"] = np.int64
        dict_types["urnr"] = np.int64
        dict_types["call"] = np.object
        dict_types["myrst"] = np.int64
        dict_types["mynr"] = np.int64
        dict_types["ismult"] = np.int64

        self.log_path = "{output_folder}/{contest_type}_{year}_{mode}_{callsign}/".format(
            output_folder=self.output_folder, contest_type=self.contest, year=self.year,
            mode=self.mode, callsign=self.callsign)
        self.log_name = "log_{contest_type}_{year}_{mode}_{callsign}.log".format(
            output_folder=self.output_folder,
            contest_type=self.contest, year=self.year,
            mode=self.mode, callsign=self.callsign)

        logging.info("Importing contest object")
        # Check if formatted pickle file exists and used unless otherwise specified
        if not os.path.exists("{}/{}".format(self.log_path, self.log_name.replace(".log", ".pickle"))):
            logging.info("Checking folders and creating them")

            # Check if logfiles folder exists and create if not
            if not os.path.exists(self.log_path):
                os.makedirs(self.log_path)

            # Download log file from web
            isgood, downloadedlog = get_log(self.contest, self.callsign, self.year, self.mode)
            if not isgood:
                return isgood, False

            infile = open("{}/{}".format(self.log_path, self.log_name), "wb")
            infile.write(downloadedlog)
            infile.close()

            logging.info("Creating Pandas object")
            # Create csv file header
            csvfile = open("{}/{}".format(self.log_path, self.log_name.replace(".log", ".csv")), "w")
            csvfile.write("frequency,mode,date,time,mycall,urrst,urnr,call,myrst,mynr,stn\n")

            # Loop on lines info line by line to create data frame
            infile = open("{}/{}".format(self.log_path, self.log_name))
            lines = infile.readlines()
            for l in lines:
                line = l.split(":")[1].replace('\n', '')
                line = line[1:]
                if "QSO" in l:
                    if len(line.split()) == 10:
                        line += ",0"
                    line = ','.join(line.split()) + "\n"
                    csvfile.write(line)
            csvfile.close()
            infile.close()
            self.log = pd.read_csv("{}/{}".format(self.log_path, self.log_name.replace(".log", ".csv")), dtype=dict_types)
            os.remove("{}/{}".format(self.log_path, self.log_name.replace(".log", ".csv")))

            # Read contest information for original log file
            self.read_contest_general_info()

            # Remove downloaded log file
            os.remove("{}/{}".format(self.log_path, self.log_name))

            return isgood, True

        return True, False

    def read_contest_general_info(self):
        infile = open("{}/{}".format(self.log_path, self.log_name))
        infile.seek(0)
        lines = infile.readlines()
        for l in lines:
            line = l.split(":")[1].replace('\n', '')
            line = line[1:]
            if "CONTEST" in l:
                self.cat_contest = line
            if "CATEGORY-OPERATOR" in l:
                self.cat_operator = line
            if "CATEGORY-ASSISTED" in l:
                self.cat_assisted = line
            if "CATEGORY-BAND" in l:
                self.cat_band = line
            if "CATEGORY-POWER" in l:
                self.cat_power = line
            if "CATEGORY-TRANSMITTER" in l:
                self.cat_transmitter = line
            if "NAME" in l:
                self.name = line
            if "LOCATION" in l:
                self.location = line
            if "OPERATORS" in l:
                self.operators = line.split()
            if "CLUB" in l:
                self.club = line
        infile.seek(0)
        self.category = "{} {} {} {} {} {}".format(
            self.cat_operator,
            self.cat_transmitter,
            self.cat_band,
            self.cat_assisted,
            self.cat_power,
            self.mode
        )
        infile.close()
