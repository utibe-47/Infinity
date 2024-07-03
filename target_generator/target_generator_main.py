import numpy as np
import pandas as pd
from typing import Optional

from data_handler.database.position_handler import PositionHandler
from target_generator.target_generator import TargetGenerator
from target_generator.target_generator_helpers import read_prices, get_allocations, get_signals, get_aum


def check_input_variables(prices, strategy_allocations, signals, aum):
    if prices is None:
        prices = read_prices()
    if signals is None:
        signals = get_signals()
    if strategy_allocations is None:
        strategy_allocations = get_allocations()
    if aum is None:
        aum = get_aum()
    return prices, strategy_allocations, signals, aum


DF = pd.DataFrame


class TradingTargetsBuilder:

    def __init__(self):
        self.prices = None
        self.signals = None
        self.strategy_allocations = None
        self.target_generator = TargetGenerator()
        self.target_position_handler = PositionHandler()

    def run(self, signals: Optional[dict] = None, prices: Optional[dict] = None, allocations: Optional[DF] = None,
            aum: Optional[float] = None) -> DF:
        prices, strategy_allocations, signals, aum = check_input_variables(prices, allocations, signals, aum)
        target_weights = self.generate_targets(signals, allocations, prices)
        self.save_targets(target_weights)
        return target_weights

    def generate_targets(self, signals: dict, allocations: np.array, prices: dict) -> DF:
        self.target_generator.prices = self.prices
        trading_targets = self.target_generator.run(signals, allocations, prices)
        return trading_targets

    def save_targets(self, target_positions: pd.DataFrame) -> None:
        self.target_position_handler.save_position(target_positions)
