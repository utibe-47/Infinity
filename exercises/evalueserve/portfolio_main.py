from evalueserve.portfolio import Portfolio


class PortfolioMain:

    def __init__(self, prices, units):
        self.prices = prices
        self.units = units
        self._weights = None
        self.rebalancing_dates = None
        self.portfolio = Portfolio(self.prices, self.units)
        self.basket_value = []
        self.basket_unit = []

    def run(self):
        self.create_portfolio()
        portfolio = self.retrieve_portfolio()
        return portfolio

    def create_portfolio(self):
        self.portfolio.create()

    def retrieve_portfolio(self):
        portfolio = self.portfolio.cache
        return portfolio
