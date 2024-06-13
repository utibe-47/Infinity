import logging
from functools import wraps
from os.path import dirname, abspath, join

import pandas as pd


def write_to_csv(filename: str, data: pd.DataFrame):
    data.to_csv(filename, encoding='utf-8')


def initialise_basket_parameters(equity_notional: float, initial_basket_value: float) -> tuple:
    basket_unit = []
    basket_value = []
    initial_basket_unit = equity_notional/initial_basket_value
    basket_unit.append(initial_basket_unit)
    basket_value.append(initial_basket_value)
    return basket_unit, basket_value


def calculate_basket_value(previous_basket_value, price, previous_price, previous_units):
    basket_value = previous_basket_value * (previous_units.mul(price).sum(axis=1)[0]/previous_units.mul(previous_price).sum(axis=1)[0])
    return basket_value


def calculate_basket_units(basket_value, previous_basket_unit, current_units, previous_units, price):
    unit_diff = current_units - previous_units
    basket_unit = previous_basket_unit + (unit_diff.mul(price).sum(axis=1)[0]/basket_value)
    return basket_unit


def calculate_daily_units(current_units: pd.DataFrame, basket_unit: float) -> pd.DataFrame:
    prime_units = current_units/basket_unit
    return prime_units


def calculate_basket_parameters(prices, units, equity_notional, initial_basket_value):
    rebalance_count = 0
    daily_units = []
    basket_units, basket_values = initialise_basket_parameters(equity_notional, initial_basket_value)
    for count, (price_date, row) in enumerate(prices.iterrows()):
        if count == 0:
            initial_units = units.iloc[[0]].reset_index(drop=True)
            initial_daily_units = calculate_daily_units(initial_units, basket_units[0])
            daily_units.append(initial_daily_units)
            continue
        previous_basket_value = basket_values[count-1]
        previous_price = prices.iloc[[count-1]].reset_index(drop=True)
        price = prices.iloc[[count]].reset_index(drop=True)
        if rebalance_count + 1 < units.shape[0]:
            next_rebalance_date = units.index[rebalance_count+1]
            if price_date == next_rebalance_date:
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
        daily_unit = calculate_daily_units(current_units, basket_unit)

        basket_values.append(basket_value)
        basket_units.append(basket_unit)
        daily_units.append(daily_unit)

    _daily_units = pd.concat(daily_units)
    _daily_units.index = prices.index
    return basket_values, basket_units, _daily_units


class PortfolioMain:

    def __init__(self, prices, units):
        self.prices = prices
        self.units = units
        self.logger = logging.getLogger(__name__)

    def run(self, equity_notional: float, initial_basket_value: float) -> dict:
        basket_values, basket_units, daily_units = self.create_portfolio(equity_notional, initial_basket_value)
        self.write_outputs_to_file(basket_values, basket_units, daily_units)
        index_output = {'index_level': basket_values, 'index_units': basket_units, 'daily_units': daily_units}
        return index_output

    def create_portfolio(self, equity_notional, initial_basket_value) -> tuple:
        basket_values, basket_units, daily_units = calculate_basket_parameters(self.prices, self.units,
                                                                               equity_notional,
                                                                               initial_basket_value)

        basket_values = pd.DataFrame(basket_values, columns=['BasketValues'], index=self.prices.index)
        basket_units = pd.DataFrame(basket_units, columns=['BasketUnits'], index=self.prices.index)
        return basket_values, basket_units, daily_units

    @staticmethod
    def write_outputs_to_file(basket_values, basket_units, daily_units):
        write_to_csv('basket_values.csv', basket_values)
        write_to_csv('basket_units.csv', basket_units)
        write_to_csv('daily_units.csv', daily_units)


def data_processor(func):
    @wraps(func)
    def wrapper_(*args, **kwargs):
        output = func(*args, **kwargs)
        processed_output = process_input_data(*output)
        return processed_output
    return wrapper_


def process_input_data(prices: pd.DataFrame, units: pd.DataFrame) -> tuple:
    units_column = list(units.columns)
    units_column[0] = 'Instruments'
    units.columns = units_column
    dates = pd.to_datetime(prices['Date'], format='%d-%b-%y')
    prices['Date'] = dates
    prices.set_index('Date', inplace=True)
    prices = prices.ffill()
    units.set_index('Instruments', inplace=True)
    units = units.T
    weight_dates = pd.to_datetime(units.index, format='%d-%b-%y')
    units.index = weight_dates
    return prices, units


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
        self.data_reader = DataReader()
        self._run_data_reader()
        self.portfolio_index_main = PortfolioMain(self.prices, self.units)

    def build_index(self, equity_notional: float, initial_basket_value: float) -> dict:
        portfolio_index = self.portfolio_index_main.run(equity_notional, initial_basket_value)
        return portfolio_index

    @data_processor
    def read_files(self) -> tuple:
        prices = self.data_reader.read_csv_pd(self.pricing_file)
        units = self.data_reader.read_csv_pd(self.units_file)
        return prices, units

    def _run_data_reader(self):
        self.prices, self.units = self.read_files()


if __name__ == '__main__':
    price_file = 'prices.csv'
    weights_file = 'Units.csv'
    _equity_notional = 7.3453215
    _initial_basket_value = 1000.00
    algo = IndexAlgorithm(price_file, weights_file)
    index = algo.build_index(_equity_notional, _initial_basket_value)
