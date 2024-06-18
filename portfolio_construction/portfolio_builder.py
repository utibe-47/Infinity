import numpy as np

from portfolio_construction.portfolio_optimizer import PortfolioOptimizer
from portfolio_construction.target_generator import TargetGenerator


class PortfolioBuilder:

    def __init__(self):
        self.prices = None
        self.strategy_allocator = PortfolioOptimizer()
        self.target_generator = TargetGenerator()

    def run(self, signals: dict, prices: dict):
        self.prices = prices
        strategy_allocations = self.calculate_strategy_allocation(signals, prices)
        target_weights = self.generate_targets(signals, strategy_allocations)
        return target_weights

    def calculate_strategy_allocation(self, signals: dict, prices: dict) -> np.array:
        strategy_allocations = self.strategy_allocator.run(signals, prices)
        return strategy_allocations

    def generate_targets(self, signals: dict, allocations: np.array) -> np.array:
        self.target_generator.prices = self.prices
        target_weights = self.target_generator.run(signals, allocations)
        return target_weights
