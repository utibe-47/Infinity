import numpy as np
import pandas as pd
import quantstats

DF = pd.DataFrame


def simple_returns(data: DF, holding_period: int = 0, freq: str = 'D') -> pd.DataFrame:
    if freq == 'D':
        offset = 1
    elif freq == 'bidiurnal':
        offset = 2
    elif freq == 'W':
        offset = 5
    elif freq == 'M':
        offset = 1
        data = data.resample('BM', how=lambda x: x[-1])
    else:
        offset = 1

    data = data.pct_change(periods=offset, fill_method='pad')
    if holding_period == 0:
        data = data.pct_change(periods=offset, fill_method='pad')
        data = data.iloc[offset:]
    else:
        offset = holding_period
        data = data.pct_change(periods=offset, fill_method='pad')
        data = data.shift(-holding_period)
        data = data[:-holding_period]
    data.replace([np.NaN, np.nan, np.inf, -np.inf, -1], 0, inplace=True)
    return data


def cumulative_returns(data: pd.DataFrame):
    returns = (1 + data).cumprod() - 1
    return returns


def log_returns(data):
    pass


def sharpe_ratio(data):
    pass


def treynor_ratio(data):
    pass


def drawdown(data):
    pass


def calmer_ratio(data):
    pass
