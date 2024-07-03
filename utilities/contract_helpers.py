from collections import defaultdict
from copy import deepcopy

import numpy as np

from commodity_trend_mappings import futures_month_code


def extract_tenor(input_str):
    if 'Index' in input_str:
        pattern = ' Index'
    else:
        pattern = ' Comdty'
    _str = input_str.replace(pattern, '')
    if len(_str) == 4:
        tenor = _str[-2:]
    elif len(_str) == 5:
        try:
            int(_str[3])
        except ValueError:
            tenor = _str[-2:]
        else:
            tenor = _str[-3:]
    else:
        tenor = _str[-3:]

    if len(_str) <= 4:
        code = _str[:2].strip()
    else:
        try:
            int(_str[3])
        except ValueError:
            code = _str[:3].strip()
        else:
            code = _str[:2].strip()

    return code, tenor, pattern


def create_tenor_dict(tenor_list):
    code_dict = defaultdict(list)
    pattern_dict = {}
    for code, tenor, pattern in tenor_list:
        if code in code_dict:
            code_dict[code].append(tenor)
        else:
            code_dict[code] = [tenor]
        if code not in pattern_dict:
            pattern_dict[code] = pattern
    return code_dict, pattern_dict


def remove_header_spaces(data_df):
    columns = list(data_df.columns)
    columns = list(map(lambda x: x.strip().replace(' ', ''), columns))
    data_df.columns = columns
    return data_df


def select_by_instrument_type(data_df, instrument_type, is_match=True):
    if is_match:
        data_df = data_df[data_df.InstrumentType == instrument_type]
    else:
        data_df = data_df[data_df.InstrumentType != instrument_type]
    data_df.reset_index(drop=True, inplace=True)
    return data_df


def separate_futures(ticker_data):
    ticker_data_future = deepcopy(ticker_data)
    ticker_data_future = remove_header_spaces(ticker_data_future)
    ticker_data_future = select_by_instrument_type(ticker_data_future, 'FUTURE')

    non_ticker_data_future = deepcopy(ticker_data)
    non_ticker_data_future = remove_header_spaces(non_ticker_data_future)
    non_ticker_data_future = select_by_instrument_type(non_ticker_data_future, 'FUTURE', is_match=False)
    return ticker_data_future, non_ticker_data_future


def find_latest_month_index(tenor_list):
    inv_futures_month_code = {v: k for k, v in futures_month_code.items()}
    month_values = list(map(lambda x: inv_futures_month_code[x[0]], tenor_list))
    max_value = max(month_values)
    max_month_index = month_values.index(max_value)
    return max_month_index


def find_latest_contract(list_held_tickers):
    tenor_list = list(map(extract_tenor, list_held_tickers))
    tenor_dict, pattern_dict = create_tenor_dict(tenor_list)

    ticker_list = []
    for code, tenor_list in tenor_dict.items():
        max_month_index = find_latest_month_index(tenor_list)

        tenor_num = [int(x[1:]) for x in tenor_list]
        max_num = max(tenor_num)
        if all(num == tenor_num[0] for num in tenor_num):
            max_index = max_month_index
        else:
            tenor_list = list(filter(lambda x: int(x[1:]) == max_num, tenor_list))
            max_index = find_latest_month_index(tenor_list)

        if len(code) == 1:
            ticker = code + " " + tenor_list[max_index] + pattern_dict[code]
        else:
            ticker = code + tenor_list[max_index] + pattern_dict[code]
        ticker_list.append(ticker)
    return ticker_list


def find_latest_non_future_data(non_future_data):
    non_future_data['Future/Security'] = non_future_data['Future/Security'].apply(
        lambda x: np.nan if bool(x) is False else x)
    non_future_data = non_future_data.dropna(subset=['Future/Security'])
    non_future_data = non_future_data.sort_values(by=['Strategy', 'Account', 'Future/Security', 'Date'])
    non_future_data.drop_duplicates(subset=['Strategy', 'Account', 'Future/Security', 'Date'], keep='first',
                                    inplace=True)
    return non_future_data
