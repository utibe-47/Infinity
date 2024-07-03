import math
from datetime import datetime
from typing import Dict

import numpy as np
import pandas as pd

from target_generator.target_generator_helpers import check_trade_direction


def round_target(target):
    if target < 0:
        target = math.ceil(target)
    else:
        target = math.floor(target)
    return target


DF = pd.DataFrame


class TargetGenerator:

    def __init__(self):
        self.prices = None
        self.aum = None

    def run(self, signals: dict, allocations: DF, prices: Dict[str, DF], aum: float) -> pd.DataFrame:
        self.prices = prices
        self.aum = aum
        targets = self.generate_targets(signals, allocations)
        return targets

    def generate_targets(self, signals, allocations) -> pd.DataFrame:
        targets_pd = pd.concat(signals.values(), keys=signals.keys()).reset_index(names=['Strategy', 'index'])
        targets_pd = targets_pd.drop(columns=['index'])
        allocations_dict = dict(zip(allocations.Strategy, allocations.Weight))
        targets_pd.loc[:, 'allocation'] = targets_pd['Strategy'].map(allocations_dict)
        targets_pd.loc[:, 'instrument_notional'] = targets_pd.apply(lambda x: self.calculate_notional(
            x.Signal, x.allocation), axis=1)
        targets_pd['TargetPositions'] = targets_pd.apply(lambda x: self.calculate_targets(
            x.Ticker, x.instrument_notional), axis=1)
        targets_pd['LeadDirection'] = targets_pd['TargetPositions'].apply(check_trade_direction)
        targets_pd['Date'] = np.array([datetime.now()] * targets_pd.shape[0])

        return targets_pd

    def calculate_notional(self, signal: float, allocation: float) -> float:
        inst_notional = self.aum * signal * allocation
        return inst_notional

    def calculate_targets(self, ticker: str, instrument_notional: float) -> float:
        price = self.prices[ticker]
        price = price['Close'][-1]
        target = instrument_notional / price
        target = round_target(target)
        return target
