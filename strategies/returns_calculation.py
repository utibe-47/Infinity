import numpy as np
import pandas as pd

DF = pd.DataFrame


def calculate_returns(df: DF, holding_period: int = 0, freq: str = 'D') -> pd.DataFrame:
    if freq == 'D':
        offset = 1
    elif freq == 'bidiurnal':
        offset = 2
    elif freq == 'W':
        offset = 5
    elif freq == 'M':
        offset = 1
        df = df.resample('BM', how=lambda x: x[-1])
    else:
        offset = 1

    df = df.pct_change(periods=offset, fill_method='pad')
    if holding_period == 0:
        df = df.pct_change(periods=offset, fill_method='pad')
        df = df.iloc[offset:]
    else:
        offset = holding_period
        df = df.pct_change(periods=offset, fill_method='pad')
        df = df.shift(-holding_period)
        df = df[:-holding_period]
    df.replace([np.NaN, np.nan, np.inf, -np.inf, -1], 0, inplace=True)
    return df
