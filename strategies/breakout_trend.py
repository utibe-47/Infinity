from strategies.returns_calculation import calculate_returns


class BreakoutTrend:

    def __init__(self, data):
        self.data = data
        self.returns = None
        self.signals = None
        self.weights = None

    def preprocess_data(self):
        self.returns = calculate_returns(self.data)

    def create_signals(self):
        pass

    def calculate_weights(self):
        pass


