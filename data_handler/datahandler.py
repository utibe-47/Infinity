from os import getcwd
from os.path import join

import pandas as pd

from data_handler.clean_data import clean_position_data, clean_exogenous_data, clean_insurance_data


def read_data(filepath):
    try:
        _data = pd.read_csv(filepath)
    except Exception:
        raise Exception('Cannot read csv file at path {}'.format(filepath))
    return _data


class DataHandler:

    def __init__(self):
        cwd = getcwd()
        self.insurance_filename = "insurancedata.csv"
        self.position_filename = "positioning.csv"
        self.exogenous_filename = "exogenous.csv"
        self.insurance_filepath = join(cwd, self.insurance_filename)
        self.position_filepath = join(cwd, self.position_filename)
        self.exogenous_filepath = join(cwd, self.exogenous_filename)
        self.us_insurance_data = None
        self.eu_insurance_data = None
        self.insurance_data = None
        self.position_data = None
        self.exogenous_data = None

    def run(self):
        data = self.read_data()
        [self.us_insurance_data, self.eu_insurance_data, self.position_data, self.exogenous_data,
         self.insurance_data] = self.clean_data(*data)

    def read_data(self):
        insurance_data = read_data(self.insurance_filepath)
        position_data = read_data(self.position_filepath)
        exogenous_data = read_data(self.exogenous_filepath)
        return insurance_data, position_data, exogenous_data

    @staticmethod
    def clean_data(insurance_data, position_data, exogenous_data):
        us_insurance_data, eu_insurance_data, insurance_data = clean_insurance_data(insurance_data)
        position_data = clean_position_data(position_data)
        exogenous_data = clean_exogenous_data(exogenous_data)
        return us_insurance_data, eu_insurance_data, position_data, exogenous_data, insurance_data
