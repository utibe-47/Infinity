import numpy as np
import pandas as pd

DF = pd.DataFrame


def get_inverse_vol_weights(df: DF, window: int = 252) -> DF:
    df = df.rolling(window=window).std()
    df = df[window:]
    df = 1 / df
    df = df.replace([np.inf], np.NaN)
    df = df.div(df.sum(axis=1, skipna=True), axis=0)
    df.fillna(0, inplace=True)
    return df


def get_equally_weight(df: DF):

    df_weights = pd.DataFrame(np.tile(1 / df.shape[1], df.shape),
                              index=df.index,
                              columns=df.columns)
    return df_weights
