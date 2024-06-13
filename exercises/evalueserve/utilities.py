from functools import wraps
import csv
import pandas as pd


def data_processor(func):
    @wraps(func)
    def wrapper_(*args, **kwargs):
        output = func(*args, **kwargs)
        processed_output = process_input_data(*output)
        return processed_output

    return wrapper_


def process_input_data(prices, weights):
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


def write_to_csv(filename, data):
    with open(filename + '.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
