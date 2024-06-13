import numpy as np
import pandas as pd

DF = pd.DataFrame


def get_inverse_vol_weights(returns: DF, window: int = 252) -> DF:
    vol = returns.rolling(window=window).std()
    vol = vol[window:]
    _weights = 1 / vol
    _weights = _weights.replace([np.inf], np.NaN)
    _weights = _weights.div(_weights.sum(axis=1, skipna=True), axis=0)
    _weights.fillna(0, inplace=True)
    return _weights


def get_equally_weight(df: DF):

    df_weights = pd.DataFrame(np.tile(1 / df.shape[1], df.shape),
                              index=df.index,
                              columns=df.columns)
    return df_weights
