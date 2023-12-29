from os import getcwd
from os.path import join

import pandas as pd
from dateutil.parser import parse


def read_data(filepath):
    try:
        _data = pd.read_csv(filepath)
    except Exception:
        raise Exception('Cannot read csv file at path {}'.format(filepath))
    return _data


def refactor_headers(data):
    columns = list(data.columns)
    columns[0] = 'Date'
    data.columns = columns
    data['Date'] = data['Date'].apply(parse)
    data.set_index(columns[0], inplace=True)
    columns.pop(0)
    return data, columns


def clean_position_data(data):
    data, _ = refactor_headers(data)
    data.columns = ['Positions']
    return data


def clean_exogenous_data(data):
    data, columns = refactor_headers(data)
    data = data.fillna(method='pad')
    data.dropna(inplace=True)
    return data


def clean_insurance_data(data):
    data, columns = refactor_headers(data)
    us_contracts = list(filter(lambda x: 'US' in x, columns))
    us_data = data.copy(deep=True)
    us_data = us_data[us_contracts]
    us_data = us_data.dropna(how='all')
    eu_data = data.drop(columns=us_contracts)
    eu_data = eu_data.dropna(how='all')
    eu_data = eu_data.fillna(method='pad') if eu_data.isnull().values.any() else eu_data
    us_data = us_data.fillna(method='pad') if us_data.isnull().values.any() else us_data
    return us_data, eu_data, data


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
