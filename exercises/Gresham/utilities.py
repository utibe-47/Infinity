import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import quantstats as qs
from collections import OrderedDict

DF = pd.DataFrame


def get_inverse_vol_weights(returns: DF, window: int = 252) -> DF:
    vol = returns.rolling(window=window).std()
    vol = vol[window:]
    _weights = 1 / vol
    _weights = _weights.replace([np.inf], np.NaN)
    _weights = _weights.div(_weights.sum(axis=1, skipna=True), axis=0)
    _weights.fillna(0, inplace=True)
    return _weights


def calculate_returns(data) -> DF:
    data = data.pct_change(periods=1, fill_method='pad')
    data.replace([np.NaN, np.nan, np.inf, -np.inf, -1], 0, inplace=True)
    return data


def run_pca(data):
    columns = list(data.columns)
    x = StandardScaler().fit_transform(data)
    pca = PCA()
    principal_components = pca.fit_transform(x)
    principal_df = pd.DataFrame(data=pca.components_, columns=columns)
    var_ratio = pd.DataFrame([pca.explained_variance_ratio_], columns=columns)
    return principal_df, var_ratio


def calculate_cumulative_returns(returns):
    return (1 + returns).cumprod() - 1


def calculate_sharpe_ratio(returns):
    sharpe = np.sqrt(20) * (returns.mean() / returns.std(ddof=1))
    return sharpe


def calculate_drawdown(returns, window=20):
    # daily_drawdown = returns.rolling(window, min_periods=1).apply(lambda x: x/x.cummax() - 1)
    # # daily_drawdown = returns / roll_max - 1.0
    # max_daily_drawdown = daily_drawdown.rolling(window, min_periods=1).min()
    # max_daily_drawdown.replace([np.NaN, np.nan, np.inf, -np.inf, -1], 0, inplace=True)

    drawdown = returns.rolling(window=window).apply(lambda val: ((val - val.cummax()) / val.cummax()).min())
    drawdown.replace([np.NaN, np.nan, np.inf, -np.inf, -1], 0, inplace=True)
    return drawdown


def calculate_moving_average(prices: DF, window_long: int, window_short: int, min_periods=None):
    long = prices.rolling(window_long, min_periods=min_periods).mean()
    short = prices.rolling(window_short, min_periods=min_periods).mean()
    signal = pd.DataFrame(index=prices.index, columns=prices.columns)
    signal[long >= short] = -1.
    signal[long <= short] = 1.
    signal.fillna(0., inplace=True)
    return signal


list_of_params = [{'window_long': 252, 'window_short': 8, 'allocation': .12},
                  {'window_long': 252, 'window_short': 20, 'allocation': .12},
                  {'window_long': 160, 'window_short': 10, 'allocation': .03},
                  {'window_long': 120, 'window_short': 10, 'allocation': .03},
                  {'window_long': 80, 'window_short': 5, 'allocation': .03},
                  {'window_long': 60, 'window_short': 2, 'allocation': .03}]


def create_signal(prices):
    signal = pd.DataFrame(index=prices.index, columns=prices.columns, data=0)
    for param in list_of_params:
        signal_tmp = calculate_moving_average(prices, param['window_long'], param['window_short'])
        signal_tmp = signal_tmp.mask(signal_tmp == 0).ffill()
        signal = signal + signal_tmp * param['allocation']
    return signal


def calculate_daily_weights(returns: DF, signal: DF, lookback_for_vol: int) -> DF:
    weights = get_inverse_vol_weights(returns, lookback_for_vol)
    weights = (weights * signal).fillna(0.0)
    return weights


def calculate_alpha_and_beta(returns, benchmark, periods=252):
    matrix = np.cov(returns, benchmark)
    beta = matrix[0, 1] / matrix[1, 1]

    alpha = returns.mean() - beta * benchmark.mean()
    alpha = alpha * periods
    return alpha, beta


def calculate_rolling_alpha_and_beta(returns, benchmark, window, periods=20):
    df = pd.DataFrame(data={"returns": returns, "benchmark": benchmark})
    corr = df.rolling(window=window).corr().unstack()["returns"]["benchmark"]
    std = df.rolling(window=window).std() * np.sqrt(periods)
    beta = corr * std["returns"] / std["benchmark"]
    alpha = df["returns"].mean() - beta * df["benchmark"].mean()
    return alpha, beta


def calculate_rolling_parameter(returns, window, param_func):
    parameter = returns.rolling(window=window).apply(param_func)
    return parameter


def plot_returns(returns, title, y_label, x_label='Date'):
    fig, ax = plt.subplots(figsize=(18, 8))

    for i in returns.columns.values:
        ax.plot(returns[i], lw=2, label=i)

    ax.legend(loc='upper left', fontsize=10)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show(fig)


def calculate_vol(df, window, period):
    df = df.rolling(window=window).apply(np.std) * np.sqrt(period)
    df = df.replace([np.inf], np.NaN)
    df.fillna(0, inplace=True)
    return df


def calculate_statistics(crypto_prices):
    crypto_returns = calculate_returns(crypto_prices)
    cum_crypto_returns = calculate_cumulative_returns(crypto_returns)

    signal = create_signal(crypto_prices)
    weights = calculate_daily_weights(crypto_returns, signal, 252)
    portfolio_returns = crypto_returns.mul(weights, axis='index').sum()
    cum_portfolio_returns = (1 + portfolio_returns).cumprod() - 1

    drawdown = calculate_drawdown(cum_crypto_returns)
    # visualize_data(crypto_prices, crypto_returns, cum_crypto_returns)
    run_pca(crypto_returns)

    crypto_correlation = crypto_returns.corr(method='pearson')
    crypto_cov = crypto_returns.cov()
    crypto_vol = calculate_vol(crypto_returns, 252)


def visualize_data(crypto_prices, crypto_returns, cum_crypto_returns):
    # Visualize crypto coin prices
    plot_returns(crypto_prices, title='Price history', y_label='Price')
    # Visualize crypto coin simple returns
    plot_returns(crypto_returns, title='Simple Crypto Returns', y_label='Simple Returns %')
    # Visualize crypto coin cumulative returns
    plot_returns(cum_crypto_returns, title='Cumulative Crypto Returns', y_label='Cumulative Returns %')
