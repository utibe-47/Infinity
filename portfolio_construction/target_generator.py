import math

import numpy as np
import pandas as pd
from typing import Optional
from datetime import datetime

from data_handler.pull_yahoo_data import YahooDataReader
from utilities.target_generator_helpers import get_signals, get_allocations, get_aum, check_trade_direction


def read_prices():
    data_reader = YahooDataReader()
    prices = data_reader.run()
    return prices


def round_target(target):
    if target < 0:
        target = math.ceil(target)
    else:
        target = math.floor(target)
    return target


class TargetGenerator:

    def __init__(self):
        self._aum = None
        self._prices = None
        self._allocations = None

    def run(self, signals: Optional[dict] = None, allocations: Optional[pd.DataFrame] = None) -> np.array:
        if signals is None:
            signals = self.signals
        if allocations is None:
            allocations = self.allocations
        targets = self.generate_targets(signals, allocations)
        return targets

    def generate_targets(self, signals, allocations) -> pd.DataFrame:
        targets_pd = pd.concat(signals.values(), keys=signals.keys()).reset_index(names=['Strategy', 'index'])
        targets_pd = targets_pd.drop(columns=['index'])
        allocations_dict = dict(zip(allocations.Strategy, allocations.Weight))
        targets_pd.loc[:, 'allocation'] = targets_pd['Strategy'].map(allocations_dict)
        targets_pd.loc[:, 'instrument_notional'] = targets_pd.apply(lambda x: self.calculate_notional(
            x.Signal, x.allocation), axis=1)
        targets_pd['Target Positions'] = targets_pd.apply(lambda x: self.calculate_targets(
            x.Ticker, x.instrument_notional), axis=1)
        targets_pd['Lead Direction'] = targets_pd['Target Positions'].apply(check_trade_direction)
        targets_pd['Date'] = np.array([datetime.now()]*targets_pd.shape[0])

        return targets_pd

    def calculate_notional(self, signal, allocation):
        inst_notional = self.aum * signal * allocation
        return inst_notional

    def calculate_targets(self, ticker, instrument_notional):
        price = self.prices[ticker]
        price = price['Close'][-1]
        target = instrument_notional/price
        target = round_target(target)
        return target

    @property
    def prices(self):
        if self._prices is None:
            self._prices = read_prices()
        return self._prices

    @prices.setter
    def prices(self, data):
        self._prices = data

    @property
    def signals(self):
        return get_signals()

    @property
    def allocations(self):
        return get_allocations()

    @property
    def aum(self):
        if self._aum is None:
            self._aum = get_aum()
        return self._aum


if __name__ == '__main__':
    target_generator = TargetGenerator()
    _targets = target_generator.run()
