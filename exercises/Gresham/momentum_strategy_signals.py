import pandas as pd

DF = pd.DataFrame

def calculate_bollinger_band_signal():
    return None


def calculate_moving_average(prices: DF, window_long: int, window_short: int, min_periods=None):
    long = prices.rolling(window_long, min_periods=min_periods).mean()
    short = prices.rolling(window_short, min_periods=min_periods).mean()
    signal = pd.DataFrame(index=prices.index, columns=prices.columns)
    signal[long >= short] = -1.
    signal[long <= short] = 1.
    signal.fillna(0., inplace=True)
    return {'df_binish_signal': signal, 'df_non_binish_signal': short - long}


def calculate_breakout_signal():
    return None