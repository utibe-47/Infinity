from evalueserve.portfolio_main import PortfolioMain


class Index:

    def __init__(self, prices, units):
        self.prices = prices
        self.weights = None
        self.units = units
        self.portfolio_main = PortfolioMain(self.prices, self.units)

    def run(self):
        self.create_portfolio()

    def create_portfolio(self):
        self.portfolio_main.create_portfolio()
        self.update_portfolio()

    def update_portfolio(self):
        level = self.portfolio_main.update_portfolio()



