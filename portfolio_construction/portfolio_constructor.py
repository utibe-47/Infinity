import numpy as np
import pandas as pd

from data_handler.tickers import STRATEGY_LIST


class PortfolioConstructor:

    def __init__(self):
        pass

    def run(self, signals, prices):
        strategy_allocations = self.get_allocations()
        return strategy_allocations

    def get_allocations(self) -> pd.DataFrame:
        allocations = np.random.random(size=len(STRATEGY_LIST))
        allocations = allocations / allocations.sum()
        allocations = pd.DataFrame(allocations, index=STRATEGY_LIST, columns=['Weight']).reset_index(names=['Strategy'])
        return allocations
