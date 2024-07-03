from data_handler.pull_yahoo_data import YahooDataReader
from target_generator.target_generator_main import PortfolioBuilder
from strategies.strategy_runner import StrategyRunner


class Algorithm:

    def __init__(self):
        self.data_reader = YahooDataReader()
        self.strategy_runner = StrategyRunner()
        self.portfolio_builder = PortfolioBuilder()

    def run(self):
        ticker_data = self.run_data_reader()
        strategy_signals = self.run_strategies(ticker_data)
        target_weights = self.construct_portfolio(strategy_signals, ticker_data)
        return target_weights

    def run_data_reader(self):
        ticker_data = self.data_reader.run()
        return ticker_data

    def run_strategies(self, ticker_data: dict):
        strategy_signals = self.strategy_runner.run(ticker_data)
        return strategy_signals

    def construct_portfolio(self, signals: dict, prices: dict):
        target_weights = self.portfolio_builder.run(signals, prices)
        return target_weights


if __name__ == '__main__':
    algo = Algorithm()
    algo.run()
