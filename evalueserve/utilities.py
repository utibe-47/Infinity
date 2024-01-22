from functools import wraps, partial
from datetime import datetime
import pandas as pd
import numpy as np
from dateutil.parser import parse


def convert_to_datetime_no_error(_date):
    try:
        date_ = parse(_date)
    except Exception:
        if isinstance(_date, datetime):
            date_ = _date
        elif isinstance(_date, np.datetime64):
            date_ = _date.astype(datetime)
        else:
            date_ = None
    return date_


def change_date_str(_date, format_string='%d/%m/%Y'):
    date_ = parse(_date)
    return date_.strftime(format_string)


def change_df_index_date_func(array):
    array = list(map(partial(change_date_str, format_string='%d/%m/%Y'), list(array)))
    array = pd.to_datetime(array, format='%d/%m/%Y')
    return array


def return_dataframe(func):
    @wraps(func)
    def wrapper_(*args, **kwargs):
        value = func(*args, **kwargs)
        result = pd.DataFrame(value[1:])
        result.columns = value[0]
        result.set_index(value[0][0], inplace=True)
        try:
            result[result.columns] = result[result.columns].apply(pd.to_numeric, errors='coerce', raw=False)
        except Exception:
            for index, row in result.iterrows():
                result.loc[index] = pd.to_numeric(row)
        if all(isinstance(val, datetime) or isinstance(convert_to_datetime_no_error(val), datetime) for val in result.index):
            result.index = change_df_index_date_func(result.index)
        return result
    return wrapper_


def return_dataframe_with_dt(func):
    @wraps(func)
    def wrapper_(*args, **kwargs):
        value = func(*args, **kwargs)
        result = pd.DataFrame(value[1:])
        result.columns = value[0]
        try:
            result[result.columns[1:]] = result[result.columns[1:]].apply(pd.to_numeric, errors='coerce', raw=False)
        except ValueError:
            for index, row in result.iterrows():
                result.loc[index] = pd.to_numeric(row)
        result.iloc[:, 0] = change_df_index_date_func(result.iloc[:, 0])
        return result
    return wrapper_


def return_dataframe_without_dt(func):
    @wraps(func)
    def wrapper_(*args, **kwargs):
        value = func(*args, **kwargs)
        result = pd.DataFrame(value[1:])
        result.columns = value[0]
        result.set_index(value[0][0], inplace=True)
        try:
            result[result.columns] = result[result.columns].apply(pd.to_numeric, errors='coerce', raw=False)
        except ValueError:
            for index, row in result.iterrows():
                result.loc[index] = pd.to_numeric(row)
        result.index = change_df_index_date_func(result.index)
        return result
    return wrapper_


def data_processor(func):
    @wraps(func)
    def wrapper_(*args, **kwargs):
        output = func(*args, **kwargs)
        processed_output = process_input_data(*output)
        return processed_output
    return wrapper_


def process_input_data(prices, weights):
    weights_column = list(weights.columns)
    weights_column.pop(0)
    weights = weights[weights_column]
    dates = prices['DATE']
    prices.set_index('DATE', inplace=True)
    weights.index = prices.index
    return prices, weights


def weights_generator(count):
    random_numbers = np.random.rand(count)
    random_numbers = random_numbers / random_numbers.sum()
    return random_numbers


def weights_creator(n_rows, n_columns):
    columns = ["GOLD", "WHEAT", "NIKKEI", "COPPER"]
    data_gen = [weights_generator(n_columns) for i in range(n_rows)]
    data = pd.DataFrame(data_gen, columns=columns)
    data.to_csv('portfolio_weights.csv')
