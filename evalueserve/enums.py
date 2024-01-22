from enum import Enum, unique


@unique
class WeightsCalculationMethod(Enum):
    EqualWeighted = 0
    MarketCap = 1
    PriceWeighted = 2
