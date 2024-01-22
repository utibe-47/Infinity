from evalueserve.enums import WeightsCalculationMethod
from evalueserve.portfolio_weight_calculator import PortfolioWeightCalculator


class Index:

    def __init__(self, prices, weights=None):
        self.prices = prices
        self._weights = weights
        self.weight_calculator = PortfolioWeightCalculator(self.prices)

    def calculate_weights(self):
        self._weights = self.weight_calculator.calculate()

    @property
    def weights(self):
        if self._weights is None:
            self.calculate_weights()
        return self._weights

