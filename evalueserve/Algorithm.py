from .utilities import data_processor
from evalueserve.Descriptors.meta_helpers import DescriptorNamingMeta
from evalueserve.data_reader import DataReader


class Algorithm(metaclass=DescriptorNamingMeta):

    def __init__(self, pricing_filename, weights_filename):
        self.pricing_file = pricing_filename
        self.weights_file = weights_filename
        self.data_reader = DataReader()

    def run(self):
        prices, weights = self.read_files()
        levels = self.create_index(prices, weights)

    @data_processor
    def read_files(self):
        prices = self.data_reader.read_csv_pd(self.pricing_file)
        weights = self.data_reader.read_csv_pd(self.weights_file)
        return prices, weights

    def create_index(self, prices, weights):
        levels = []
        return levels


if __name__ == '__main__':
    price_file = 'price_data.csv'
    weights_file = 'portfolio_weights.csv'
    algo = Algorithm(price_file, weights_file)
    algo.run()
