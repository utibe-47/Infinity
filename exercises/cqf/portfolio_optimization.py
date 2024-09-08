import warnings
import pandas as pd
import numpy as np
from numpy.linalg import multi_dot
from functools import partial
import yfinance as yf
import cufflinks as cf
import plotly
import plotly.express as px
from sqlalchemy import create_engine, text
import scipy.optimize as sco

np.random.seed(42)
warnings.filterwarnings('ignore')
cf.set_config_file(offline=True, dimensions=(1000, 600))
setattr(plotly.offline, "__PLOTLY_OFFLINE_INITIALIZED", True)

px.defaults.width, px.defaults.height = 1000, 600
pd.set_option('display.precision', 4)


def min_volatility(weights, returns):
    return portfolio_stats(weights, returns)[1]


def min_variance(weights, returns):
    return portfolio_stats(weights, returns)[1] ** 2


def max_sharpe_ratio(weights, returns):
    return -portfolio_stats(weights, returns)[2]


def run_optimizer():
    url = 'https://en.wikipedia.org/wiki/NIFTY_50'
    engine = create_database()
    nifty50 = read_html_data(url)
    data = read_yahoo_data(nifty50)
    # save_to_database(data, nifty50, engine)

    assets = sorted(['ICICIBANK', 'ITC', 'RELIANCE', 'TCS', 'ASIANPAINT'])
    num_of_asset = len(assets)
    num_of_portfolio = 5000

    df = query_database(assets, engine)
    df['2021':].normalize().iplot(kind='line')

    returns = df.pct_change().dropna()
    annual_returns = round(returns.mean() * 260 * 100, 2)
    annual_stdev = round(returns.std() * np.sqrt(260) * 100, 2)

    create_plots(annual_returns, annual_stdev, num_of_asset, num_of_portfolio, returns)

    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for x in range(num_of_asset))
    initial_weights = np.array(num_of_asset * [1. / num_of_asset])

    _max_sharpe_ratio = partial(max_sharpe_ratio, returns=returns)
    _min_variance = partial(min_variance, returns=returns)
    _min_volatility = partial(min_volatility, returns=returns)

    opt_sharpe = sco.minimize(_max_sharpe_ratio, initial_weights, method='SLSQP', bounds=bounds, constraints=cons)
    opt_var = sco.minimize(_min_variance, initial_weights, method='SLSQP', bounds=bounds, constraints=cons)

    target_returns = np.linspace(0.15, 0.24, 100)
    t_vols = []

    for target_return in target_returns:
        ef_cons = [{'type': 'eq', 'fun': lambda x: portfolio_stats(x, returns)[0] - target_return},
                   {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]

        opt_ef = sco.minimize(_min_volatility, initial_weights, method='SLSQP', bounds=bounds, constraints=ef_cons)
        t_vols.append(opt_ef['fun'])

    target_vols = np.array(t_vols)
    efficient_portfolio = pd.DataFrame({'target_returns': np.around(100 * target_returns, 2),
                                        'target_vols': np.around(100 * target_vols, 2),
                                        'target_sharpe': np.around(target_returns / target_vols, 2)})

    fig = px.scatter(
        efficient_portfolio, x='target_vols', y='target_returns', color='target_sharpe',
        labels={'target_returns': 'Expected Return', 'target_vols': 'Expected Volatility',
                'target_sharpe': 'Sharpe Ratio'},
        title="Efficient Frontier Portfolio").update_traces(mode='markers', marker=dict(symbol='cross'))

    fig.add_scatter(
        mode='markers',
        x=[100 * portfolio_stats(opt_sharpe['x'], returns)[1]],
        y=[100 * portfolio_stats(opt_sharpe['x'], returns)[0]],
        marker=dict(color='red', size=20, symbol='star'),
        name='Max Sharpe'
    ).update(layout_showlegend=False)

    fig.add_scatter(
        mode='markers',
        x=[100 * portfolio_stats(opt_var['x'], returns)[1]],
        y=[100 * portfolio_stats(opt_var['x'], returns)[0]],
        marker=dict(color='green', size=20, symbol='star'),
        name='Min Variance'
    ).update(layout_showlegend=False)

    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)
    fig.show()


def create_plots(annual_returns, annual_stdev, num_of_asset, num_of_portfolio, returns):
    df2 = pd.DataFrame({'Ann Ret': annual_returns, 'Ann Vol': annual_stdev})
    df2.iplot(kind='bar', shared_xaxes=True, orientation='h')
    df2.reset_index().iplot(kind='pie', labels='index', values='Ann Ret', textinfo='percent+label', hole=0.4)
    temp = portfolio_simulation(returns, num_of_portfolio, num_of_asset)
    fig = px.scatter(
        temp, x='port_vols', y='port_rets', color='sharpe_ratio',
        labels={'port_vols': 'Expected Volatility', 'port_rets': 'Expected Return', 'sharpe_ratio': 'Sharpe Ratio'},
        title="Monte Carlo Simulated Portfolio"
    ).update_traces(mode='markers', marker=dict(symbol='cross'))
    fig.add_scatter(
        mode='markers',
        x=[temp.iloc[temp.sharpe_ratio.idxmax()]['port_vols']],
        y=[temp.iloc[temp.sharpe_ratio.idxmax()]['port_rets']],
        marker=dict(color='RoyalBlue', size=20, symbol='star'),
        name='Max Sharpe'
    ).update(layout_showlegend=False)
    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)
    fig.show()


def create_database():
    engine = create_engine('sqlite:///Nifty50')
    return engine


def read_html_data(url):
    nifty50 = pd.read_html(url)[2].Symbol.to_list()
    return nifty50


def read_yahoo_data(tickers):
    data = [yf.download(symbol + '.NS', start="2019-01-01", end="2023-12-31",
                        progress=False).reset_index() for symbol in tickers]
    return data


def save_to_database(data, tickers, engine):
    for frame, symbol in zip(data, tickers):
        frame.to_sql(symbol, engine, if_exists='replace', index=False)


def query_database(assets, engine):
    df = pd.DataFrame()
    for asset in assets:
        query = f'SELECT Date, Close FROM  {asset}'
        with engine.connect() as connection:
            df1 = pd.read_sql_query(text(query), connection, index_col='Date')
            df1.columns = [asset]
        df = pd.concat([df, df1], axis=1)
    return df


def portfolio_simulation(returns, num_of_portfolio, num_of_asset):
    rets = []
    vols = []
    wts = []

    for i in range(num_of_portfolio):
        weights = np.random.random(num_of_asset)
        weights /= np.sum(weights)

        rets.append(weights.T @ np.array(returns.mean() * 260))
        vols.append(np.sqrt(multi_dot([weights.T, returns.cov() * 260, weights])))
        wts.append(weights)

    data = {'port_rets': rets, 'port_vols': vols}
    for counter, symbol in enumerate(returns.columns.tolist()):
        data[symbol + ' weight '] = [w[counter] for w in wts]

    port_df = pd.DataFrame(data)
    port_df['sharpe_ratio'] = port_df['port_rets'] / port_df['port_vols']

    return round(port_df, 4)


def portfolio_stats(weights, returns):
    weights = np.array(weights)
    portfolio_returns = weights.T @ np.array(returns.mean() * 260)
    portfolio_vols = np.sqrt(multi_dot([weights.T, returns.cov() * 260, weights]))
    return np.array([portfolio_returns, portfolio_vols, portfolio_returns / portfolio_vols])


if __name__ == '__main__':
    run_optimizer()
