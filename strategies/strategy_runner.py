from target_generator.target_generator_helpers import get_signals


class StrategyRunner:

    def __init__(self):
        self.signals = {}

    def run(self, ticker_data: dict):
        signals = get_signals()
        return signals
