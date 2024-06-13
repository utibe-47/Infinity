from os import getcwd
from os.path import join

import pandas as pd
from dateutil.parser import parse
from enum import Enum, unique


@unique
class DataParams(Enum):
    CryptoPrices = 1
    CryptoVolumes = 2
    MarketPrices = 3
    MarketVolumes = 4


data_parameters = {DataParams.CryptoPrices: None, DataParams.CryptoVolumes: None,
                   DataParams.MarketPrices: None, DataParams.MarketVolumes: None}


def read_data(filepath):
    try:
        _data = pd.read_csv(filepath)
    except Exception:
        raise Exception('Cannot read csv file at path {}'.format(filepath))
    return _data


def refactor_headers(data):
    columns = list(data.columns)
    data['Dates'] = data['Dates'].apply(parse)
    data.set_index(columns[0], inplace=True)
    data = data.apply(pd.to_numeric, errors='coerce')
    return data


def drop_all_nan_rows(prices, volumes):
    ind = list(prices.iloc[:, 1:].dropna(how='all').index)
    prices = refactor_headers(prices.loc[ind])
    volumes = refactor_headers(volumes.loc[ind])
    return prices, volumes


class DataHandler:

    def __init__(self):
        cwd = getcwd()
        self.filename = "crypto_data_set.csv"
        self.filepath = join(cwd, self.filename)
        self.num_market_instruments = 3

    def run(self):
        data = self.read_data()
        crypto_prices, crypto_volumes, market_prices, market_volumes = self.clean_data(data)
        return crypto_prices, crypto_volumes, market_prices, market_volumes

    def read_data(self):
        _data = read_data(self.filepath)
        return _data

    def clean_data(self, data):
        columns = list(data.columns)
        column_of_prices = columns[:1] + columns[1:-1:2]
        column_of_volume = columns[:1] + list(set(columns) - set(column_of_prices))
        data = data.iloc[1:]
        data = data[::-1].reset_index(drop=True)
        prices = data.loc[:, data.columns.isin(column_of_prices)]
        volumes = data.loc[:, data.columns.isin(column_of_volume)]
        volumes.columns = column_of_prices

        market_prices = pd.concat([prices.iloc[:, 0], prices.iloc[:, -self.num_market_instruments:]], axis=1)
        market_volumes = pd.concat([volumes.iloc[:, 0], volumes.iloc[:, -self.num_market_instruments:]], axis=1)

        crypto_prices = prices.iloc[:, :-self.num_market_instruments]
        crypto_volumes = volumes.iloc[:, :-self.num_market_instruments]

        crypto_prices, crypto_volumes = drop_all_nan_rows(crypto_prices, crypto_volumes)
        market_prices, market_volumes = drop_all_nan_rows(market_prices, market_volumes)

        data_parameters[DataParams.CryptoPrices] = crypto_prices
        data_parameters[DataParams.MarketPrices] = market_prices
        data_parameters[DataParams.CryptoVolumes] = crypto_volumes
        data_parameters[DataParams.MarketVolumes] = market_volumes
        return crypto_prices, crypto_volumes, market_prices, market_volumes
