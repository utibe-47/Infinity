import logging
from copy import deepcopy
from datetime import datetime

from evalueserve.level_calculations import calculate_value
from evalueserve.portfolio_weight_calculator import calculate_weight


class PortfolioComponent:

    def __init__(self, ticker, weight):
        self.ticker: str = ticker
        self.weight: float = weight


class Portfolio:

    def __init__(self, prices, units):
        self.holdings = []
        self.cache = {}
        self.source_date: datetime = datetime.today()
        self.equity_notional = 7.3453215
        self.initial_basket_value = 1000.0
        self.prices = prices
        self.units = units
        self.logger = logging.getLogger(__name__)

    def create(self):
        basket_values, basket_units, prime_units = calculate_value(self.prices, self.units, self.equity_notional,
                                                                   self.initial_basket_value)

        tickers = list(self.units.columns)
        prime_units.index = self.prices.index

        for count in range(0, prime_units.shape[0]):
            _unit = prime_units.iloc[[0]]
            basket_data = {'basket_value': basket_values[count], 'basket_unit': basket_units[count]}
            weights = calculate_weight(_unit)
            for ticker, weight in zip(tickers, weights.values.tolist()[0]):
                self.add_instrument(ticker, weight, rebalance=False)
            self.save_to_cache(self.prices.index[count], basket_data=basket_data)

    def update_weights(self, new_weights: dict):
        for ticker, weight in new_weights.items():
            if self.contains(ticker):
                index = [(ind, item) for ind, item in enumerate(self.holdings) if item.ticker == ticker][0]
                self.holdings[index[0]].weight = weight
        self.normalize()

    def add_instrument(self, ticker: str, weight: float, rebalance: bool = True):
        new = PortfolioComponent(ticker=ticker, weight=weight)
        if any([item.ticker == ticker for item in self.holdings]):
            raise ValueError(f"Instrument {ticker} already in portfolio")
        self.holdings.append(new)
        if rebalance:
            self.normalize()

    def remove_instrument(self, ticker: str):
        if self.contains(ticker):
            index = [(ind, item) for ind, item in enumerate(self.holdings) if item.ticker == ticker][0]
            self.holdings.pop(index[0])
            self.normalize()

    def exclude(self, exclusion_list: list):
        new_holdings = []
        excluded_items = []
        excluded_weight = 0.0
        for item in self.holdings:
            if item.ticker not in exclusion_list:
                new_holdings.append(item)
            else:
                excluded_items.append(item)
                excluded_weight += item.weight

        self.holdings = new_holdings
        self.normalize()
        if len(excluded_items) > 0:
            self.logger.info(f"The weights for instruments {excluded_items} were set to 0. Total value "
                             f"excluded {excluded_weight}.")

    def save_to_cache(self, date: datetime.date, basket_data: dict = None):
        holdings = deepcopy(self.holdings)
        if bool(basket_data):
            holdings.append(basket_data)
        self.cache[date] = holdings
        self.holdings = []

    def normalize(self):
        """Ensure component weights go to 100"""
        self._reweight_portfolio()

    def contains(self, ticker: str) -> bool:
        return ticker in [item.ticker for item in self.holdings]

    def _reweight_portfolio(self) -> None:
        weights: float = sum([item.weight for item in self.holdings])

        scaling_factor = 1.0 / weights
        for item in self.holdings:
            item.weight = item.weight * scaling_factor
        self.holdings = sorted(self.holdings, key=lambda x: x.weight, reverse=True)
