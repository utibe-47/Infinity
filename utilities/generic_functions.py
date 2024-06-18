import re

import pandas as pd


def create_dataframe(queried_data, *args):
    data_gen = [[getattr(obj_, arg) for arg in args] for obj_ in queried_data]
    data_df = pd.DataFrame(data_gen, columns=list(map(lambda x: x.upper(), args)))
    return data_df


def add_space_camel_case(input_str):
    return re.sub(r'\B([A-Z])', r' \1', input_str)


def num_percentage(x):
    return "{:.2f}".format(x*100) + '%'


def round_down_2dp_with_comma(x):
    return "{0:,.2f}".format(x)


def round_down_whole_number_with_comma(x):
    return "{:,.0f}".format(x)


def round_down_whole_number(x):
    return "{:.0f}".format(x)


def rounding_down_2dp(x):
    return "{:.2f}".format(x)


def get_sign(number):
    if number < 0:
        return -1
    else:
        return 1


def ordered_list_of_strings(input_data: list):

    n = len(input_data)
    output = [input_data[0]]

    for i in range(1, n):
        if len(input_data[i]) > len(output[-1]):

            output.append(input_data[i])
        else:

            low = 0
            high = len(output) - 1
            while low < high:
                mid = low + (high - low) // 2
                if output[mid] < input_data[i]:
                    low = mid + 1
                else:
                    high = mid

            output[low] = input_data[i]
    return len(output)


def clean_ticker(ticker: str):
    ticker = ticker.replace('^', '').replace('=X', '').replace('=F', '').replace('-', '')
    return ticker
