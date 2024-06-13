import logging
import csv
import pandas as pd

from copy import deepcopy
from datetime import datetime
from functools import wraps
from os.path import dirname, abspath, join


def calculate_weight(units):
    weights = units.div(units.sum(axis=1), axis=0)
    return weights


def initialise_basket_parameters(equity_notional: float, initial_basket_value: float) -> tuple:
    basket_unit = []
    basket_value = []
    initial_basket_unit = equity_notional/initial_basket_value
    basket_unit.append(initial_basket_unit)
    basket_value.append(initial_basket_value)
    return basket_unit, basket_value


def calculate_basket_value(previous_basket_value, price, previous_price, previous_units):
    basket_value = previous_basket_value * ((previous_units.mul(price)).sum(axis=1)[0]/previous_units.mul(previous_price).sum(axis=1)[0])
    return basket_value


def calculate_basket_units(basket_value, previous_basket_unit, current_units, previous_units, price):
    basket_unit = previous_basket_unit + ((current_units - previous_units).mul(price).sum(axis=1))[0]/basket_value
    return basket_unit


def calculate_prime_units(current_units: pd.DataFrame, basket_unit: float) -> pd.DataFrame:
    prime_units = current_units/basket_unit
    return prime_units


def calculate_basket_parameters(prices, units, equity_notional, initial_basket_value):
    rebalance_count = 0
    prime_units = []
    basket_units, basket_values = initialise_basket_parameters(equity_notional, initial_basket_value)
    for count, (index, row) in enumerate(prices.iterrows()):
        if count == 0:
            initial_units = units.iloc[[0]].reset_index(drop=True)
            initial_prime_units = calculate_prime_units(initial_units, basket_units[0])
            prime_units.append(initial_prime_units)
            continue
        previous_basket_value = basket_values[count-1]
        previous_price = prices.iloc[[count-1]].reset_index(drop=True)
        price = prices.iloc[[count]].reset_index(drop=True)
        if rebalance_count + 1 < units.shape[0] and index >= units.index[rebalance_count+1]:
            rebalance_count += 1
        current_units = units.iloc[[rebalance_count]].reset_index(drop=True)
        if rebalance_count > 0:
            previous_unit_index = rebalance_count - 1
        else:
            previous_unit_index = rebalance_count
        previous_units = units.iloc[[previous_unit_index]].reset_index(drop=True)
        previous_basket_unit = basket_units[count-1]

        basket_value = calculate_basket_value(previous_basket_value, price, previous_price, previous_units)
        basket_unit = calculate_basket_units(basket_value, previous_basket_unit, current_units, previous_units, price)
        prime_unit = calculate_prime_units(current_units, basket_unit)

        basket_values.append(basket_value)
        basket_units.append(basket_unit)
        prime_units.append(prime_unit)

    prime_units = pd.concat(prime_units)
    return basket_values, basket_units, prime_units


class PortfolioComponent:

    def __init__(self, ticker, weight):
        self.ticker: str = ticker
        self.weight: float = weight


class Portfolio:

    def __init__(self, prices, units):
        self.holdings = []
        self.cache = {}
        self.prices = prices
        self.units = units
        self.logger = logging.getLogger(__name__)

    def create(self, equity_notional: float, initial_basket_value: float):
        basket_values, basket_units, prime_units = calculate_basket_parameters(self.prices, self.units,
                                                                               equity_notional,
                                                                               initial_basket_value)

        tickers = list(self.units.columns)
        prime_units.index = self.prices.index

        for count in range(0, prime_units.shape[0]):
            _unit = prime_units.iloc[[0]]
            basket_data = {'basket_value': basket_values[count], 'basket_unit': basket_units[count]}
            weights = calculate_weight(_unit)
            for ticker, weight in zip(tickers, weights.values.tolist()[0]):
                self.add_instrument(ticker, weight, rebalance=False)
            self.save_to_cache(self.prices.index[count], basket_data=basket_data)

        basket_values = pd.DataFrame(basket_values, columns=['BasketValues'], index=self.prices.index)
        basket_units = pd.DataFrame(basket_units, columns=['BasketUnits'], index=self.prices.index)
        write_to_csv('basket_values', basket_values)
        write_to_csv('basket_units', basket_units)
        write_to_csv('Prime_units', prime_units)

    def add_instrument(self, ticker: str, weight: float, rebalance: bool = True):
        new = PortfolioComponent(ticker=ticker, weight=weight)
        if any([item.ticker == ticker for item in self.holdings]):
            raise ValueError(f"Instrument {ticker} already in portfolio")
        self.holdings.append(new)
        if rebalance:
            self.normalize()

    def save_to_cache(self, date: datetime.date, basket_data: dict = None):
        holdings = deepcopy(self.holdings)
        if bool(basket_data):
            holdings.append(basket_data)
        self.cache[date] = holdings
        self.holdings = []

    def normalize(self):
        """Ensure component weights go to 100"""
        self._reweight_portfolio()

    def contains(self, ticker: str) -> bool:
        return ticker in [item.ticker for item in self.holdings]

    def _reweight_portfolio(self) -> None:
        weights: float = sum([item.weight for item in self.holdings])

        scaling_factor = 1.0 / weights
        for item in self.holdings:
            item.weight = item.weight * scaling_factor
        self.holdings = sorted(self.holdings, key=lambda x: x.weight, reverse=True)


class PortfolioMain:

    def __init__(self, prices, units):
        self.prices = prices
        self.units = units
        self._weights = None
        self.rebalancing_dates = None
        self.portfolio = Portfolio(self.prices, self.units)
        self.basket_value = []
        self.basket_unit = []

    def run(self, equity_notional: float, initial_basket_value: float) -> dict:
        self.create_portfolio(equity_notional, initial_basket_value)
        portfolio = self.retrieve_portfolio()
        return portfolio

    def create_portfolio(self, equity_notional, initial_basket_value):
        self.portfolio.create(equity_notional, initial_basket_value)

    def retrieve_portfolio(self):
        portfolio = self.portfolio.cache
        return portfolio


def write_list_to_csv(filename, data):
    with open(filename + '.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)


def write_to_csv(filename: str, data: pd.DataFrame):
    data.to_csv(filename, encoding='utf-8')


def data_processor(func):
    @wraps(func)
    def wrapper_(*args, **kwargs):
        output = func(*args, **kwargs)
        processed_output = process_input_data(*output)
        return processed_output
    return wrapper_


def process_input_data(prices: pd.DataFrame, weights: pd.DataFrame) -> tuple:
    weights_column = list(weights.columns)
    weights_column[0] = 'Instruments'
    weights.columns = weights_column
    dates = pd.to_datetime(prices['Date'], format='%d-%b-%y')
    prices['Date'] = dates
    prices.set_index('Date', inplace=True)
    weights.set_index('Instruments', inplace=True)
    weights = weights.T
    weight_dates = pd.to_datetime(weights.index, format='%d-%b-%y')
    weights.index = weight_dates
    return prices, weights


class DataReader:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def read_csv_pd(self, filename, is_full_file_path=False, folder_path=None, **kwargs) -> pd.DataFrame:
        filename = self.get_full_filename(filename, folder_path, is_full_file_path)
        try:
            csv_data = pd.read_csv(filename, **kwargs)
        except Exception as e:
            msg = 'Could not read csv file: {}, exception {} was raised'.format(filename, str(e))
            raise Exception(msg)
        return csv_data

    def get_full_filename(self, filename: str, folder_path: str, isfile_path: bool) -> str:
        if not isfile_path:
            if folder_path is None:
                filename = self._get_filepath(filename)
            else:
                filename = join(folder_path, filename)
        return filename

    def _get_filepath(self, filename: str):
        try:
            directory_name = dirname(abspath(__file__))
        except FileNotFoundError:
            raise FileNotFoundError('Could not find file {}, confirm that file exists in same directory as '
                                    '{} class'.format(filename, self.__name__))
        else:
            return join(directory_name, filename)


class IndexAlgorithm:

    def __init__(self, pricing_filename: str, weights_filename: str):
        self.pricing_file = pricing_filename
        self.units_file = weights_filename
        self.prices = None
        self.units = None
        self.portfolio_index_main = None
        self.data_reader = DataReader()
        self._run_data_reader()
        self._create_objects()

    def build_index(self, equity_notional: float, initial_basket_value: float) -> dict:
        portfolio_index = self.portfolio_index_main.run(equity_notional, initial_basket_value)
        return portfolio_index

    @data_processor
    def read_files(self) -> tuple:
        prices = self.data_reader.read_csv_pd(self.pricing_file)
        units = self.data_reader.read_csv_pd(self.units_file)
        return prices, units

    def _create_objects(self):
        self.portfolio_index_main = PortfolioMain(self.prices, self.units)

    def _run_data_reader(self):
        self.prices, self.units = self.read_files()


if __name__ == '__main__':
    price_file = 'prices.csv'
    weights_file = 'Units.csv'
    _equity_notional = 7.3453215
    _initial_basket_value = 1000.00
    algo = IndexAlgorithm(price_file, weights_file)
    index = algo.build_index(_equity_notional, _initial_basket_value)
