import numpy as np
import pandas as pd


def convert_epoch_dates(values):
    return pd.to_datetime(list(map(lambda x: (int(x) * 86400) - 2209161600, values)), unit='s')


def clean_data(data, columns):
    data.set_index(data.columns[0], inplace=True)
    data.columns = columns
    data = data.T
    return data


def read_files(filename):
    _allocations = pd.read_excel(filename, engine='pyxlsb', sheet_name='Strategic_Asset_allocation')
    _data = pd.read_excel(filename, engine='pyxlsb', sheet_name='Datasets', header=None, dtype=object)
    return _data, _allocations


def process_data(data):
    columns = data.iloc[0, 1:]
    columns = convert_epoch_dates(columns)

    total_returns = clean_data(data[1:35], columns)
    option_adjusted_spread = clean_data(data[38:72], columns)
    yield_to_worst = clean_data(data[75:109], columns)
    benchmark_weights = clean_data(data[111:145], columns)
    effective_duration = clean_data(data[148:182], columns)
    spread_duration = clean_data(data[184:], columns)
    return total_returns, option_adjusted_spread, yield_to_worst, benchmark_weights, effective_duration, spread_duration


def normalize_data(weights):
    weights[weights.columns] = weights[weights.columns] / weights[weights.columns].sum()
    return weights


def portfolio_analysis(returns, allocations, benchmark):
    benchmark = normalize_data(benchmark.T)
    allocations.set_index(allocations.columns[0], inplace=True)
    allocations = normalize_data(allocations)
    benchmark_portfolio = returns.T.mul(benchmark, axis=0).sum(axis=0) / 100
    portfolio_returns = returns.T.mul(allocations['Strategic Allocation Weights'], axis='index').sum(axis=0) / 100

    cum_benchmark_portfolio = (1 + benchmark_portfolio).cumprod() - 1
    cum_portfolio_returns = (1 + portfolio_returns).cumprod() - 1

    return portfolio_returns, benchmark_portfolio, cum_portfolio_returns, cum_benchmark_portfolio


def calculate_vol(df, window):
    df = df.rolling(window=window).apply(np.std) * np.sqrt(12)
    df = df.replace([np.inf], np.NaN)
    df.fillna(0, inplace=True)
    return df


def portfolio_volatility(portfolio_returns, benchmark_portfolio):
    portfolio_vol = calculate_vol(portfolio_returns, 12)
    benchmark_vol = calculate_vol(benchmark_portfolio, 12)
    return portfolio_vol, benchmark_vol


def carry_strategy(yield_to_worst):
    cap = 0.45
    constant_factor = 2
    yields = yield_to_worst.fillna(method='pad').iloc[:, :-2]
    yields.dropna(inplace=True)

    low_yield = yields.iloc[:, :16]
    high_yield = yields.iloc[:, 16:]

    slope = high_yield - low_yield.values
    slope_rank = slope.rank(axis=1, method='first', numeric_only=None, na_option='keep', ascending=False, pct=False)

    longs = np.where(slope_rank < 4, 1, 0)
    shorts = np.where(slope_rank > 3, -1, 0)

    high_yield_d = high_yield.diff(1, 0)
    window = high_yield_d.rolling(12)
    high_yields_vol = window.std(ddof=0) * np.sqrt(12)
    df_longs_sum = (1 / (high_yields_vol / 100) * longs).sum(axis=1)
    df_shorts_sum = (1 / (high_yields_vol / 100) * shorts).sum(axis=1)
    df_w_longs = pd.DataFrame((1 / high_yields_vol) * longs * 100).div(df_longs_sum, axis="index")
    df_w_shorts = pd.DataFrame((1 / high_yields_vol) * shorts * 100).div(df_shorts_sum, axis="index")
    df_w_longs = pd.DataFrame(np.where(df_w_longs > cap, cap, df_w_longs))
    df_w_shorts = pd.DataFrame(np.where(df_w_shorts > cap, cap, df_w_shorts))

    for x in range(0, len(df_w_longs)):

        z = (1 - df_w_longs.iloc[x].sum()) / df_w_longs.iloc[x].where(df_w_longs.iloc[x] < cap).sum()

        z1 = (1 - df_w_shorts.iloc[x].sum()) / df_w_shorts.iloc[x].where(df_w_shorts.iloc[x] < cap).sum()

        for y in range(0, len(df_w_longs.columns)):

            if cap > df_w_longs.iloc[x, y] > 0:
                df_w_longs.iloc[x, y] = df_w_longs.iloc[x, y] * (1 + z)
            else:
                df_w_longs.iloc[x, y] = df_w_longs.iloc[x, y]

            if cap > df_w_shorts.iloc[x, y] > 0:
                df_w_shorts.iloc[x, y] = df_w_shorts.iloc[x, y] * (1 + z1)
            else:
                df_w_shorts.iloc[x, y] = df_w_shorts.iloc[x, y]

    weights = (df_w_longs * longs) + (df_w_shorts * shorts)
    weights.columns = list(high_yield.columns)
    weights.index = list(high_yield.index)
    weights = constant_factor * weights
    return weights


def strategy_portfolio_analysis(weights, returns):
    weights = weights.dropna()
    _returns = returns[weights.columns]
    _returns = _returns[_returns.index.isin(weights.index)]
    portfolio_returns = _returns.mul(weights, axis='index').sum(axis=1) / 100
    cum_portfolio_returns = (1 + portfolio_returns).cumprod() - 1
    return cum_portfolio_returns * 100


if __name__ == '__main__':
    filename = "Credit_Data.xlsb"
    input_data, allocations = read_files(filename)
    total_returns, option_adjusted_spread, yield_to_worst, benchmark_weights, effective_duration, spread_duration = process_data(
        input_data)
    weights = carry_strategy(yield_to_worst)
    carry_returns = strategy_portfolio_analysis(weights, total_returns)
    portfolio_returns, benchmark_portfolio, cum_portfolio_returns, cum_benchmark_portfolio = portfolio_analysis(
        total_returns, allocations, benchmark_weights)
    portfolio_vol, benchmark_vol = portfolio_volatility(portfolio_returns.to_frame(), benchmark_portfolio.to_frame())
