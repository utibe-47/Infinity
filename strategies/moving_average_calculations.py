from itertools import combinations

import numpy as np
import pandas as pd
from pandas._libs.tslibs.offsets import Week


def create_span_combinations(min_span, max_span, span_step):
    span_values = np.arange(min_span, max_span, span_step)
    span_combinations = list(combinations(span_values, 2))
    return span_combinations


Df = pd.DataFrame


def exponential_weighted_moving_average(data: Df, span: int):
    return data.ewm(span=span).mean()


def ewma_cross(data, short, long, header=''):
    cross = exponential_weighted_moving_average(data, short) - exponential_weighted_moving_average(data, long)
    cross.columns = [header]
    return cross


def create_signal_combinations(data, span_combinations):
    signal_list = []
    for comb in span_combinations:
        short, long = comb
        label = "{}_{}".format(short, long)
        signal_list.append(ewma_cross(data, short, long, header=label))
    combined_signal = pd.concat(signal_list, axis=1)
    return combined_signal


def compile_dataset(position_data, signals):
    signals['week_year'] = signals['week_endings'] = signals.index + Week(weekday=4)
    signals_df = signals.groupby(['week_endings']).sum(numeric_only=True)
    position_data = position_data[position_data.index.isin(signals_df.index)]
    missing_position_dates = np.array(list(set(signals_df.index) - set(position_data.index)))
    if len(missing_position_dates) > 0:
        ind = \
            np.where(
                (missing_position_dates >= signals_df.index[0]) & (missing_position_dates <= position_data.index[-1]))[
                0]
        if len(ind) > 0:
            nan_df = pd.DataFrame([np.nan] * len(ind), index=missing_position_dates[ind],
                                  columns=list(position_data.columns))
            position_data = pd.concat([position_data, nan_df])
            position_data = position_data.sort_index(ascending=True)
            position_data = position_data.fillna(method='pad')
    signals_df = signals_df[signals_df.index.isin(position_data.index)]
    position_data.columns = ['Positions']
    dataset = pd.concat([position_data, signals_df], axis=1)
    return dataset
