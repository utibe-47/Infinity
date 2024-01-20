import numpy as np
import pandas as pd


DF = pd.DataFrame


def volatility_calculator(returns: DF, window):
    returns = returns.rolling(window=window).apply(np.std) * np.sqrt(12)
    returns = returns.replace([np.inf], np.NaN)
    returns.fillna(0, inplace=True)
    return returns


class PortfolioAnalytics:

    def __init__(self):
        pass

    @staticmethod
    def calculate_cumulative_returns(returns: DF, weights: DF) -> DF:
        portfolio_returns = returns.mul(weights, axis='index').sum(axis=1) / 100
        cum_portfolio_returns = (1 + portfolio_returns).cumprod() - 1
        return cum_portfolio_returns * 100

    def calculate_volatility(self, portfolio_returns: DF) -> DF:
        portfolio_vol = self._volatility_calculator(portfolio_returns, 12)
        return portfolio_vol

    @staticmethod
    def _volatility_calculator(returns: DF, window: int) -> DF:
        returns = returns.rolling(window=window).apply(np.std) * np.sqrt(12)
        returns = returns.replace([np.inf], np.NaN)
        returns.fillna(0, inplace=True)
        return returns
