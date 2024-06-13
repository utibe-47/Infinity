from evalueserve.Descriptors.meta_helpers import DescriptorNamingMeta
from evalueserve.data_reader import DataReader
from evalueserve.portfolio_main import PortfolioMain
from evalueserve.utilities import data_processor


class Algorithm(metaclass=DescriptorNamingMeta):

    def __init__(self, pricing_filename, weights_filename):
        self.pricing_file = pricing_filename
        self.units_file = weights_filename
        self.prices = None
        self.units = None
        self.portfolio_index_main = None
        self.data_reader = DataReader()
        self._get_data()
        self._create_objects()

    def run(self):
        index = self.generate_index()

    @data_processor
    def read_files(self):
        prices = self.data_reader.read_csv_pd(self.pricing_file)
        units = self.data_reader.read_csv_pd(self.units_file)
        return prices, units

    def generate_index(self):
        portfolio_index = self.portfolio_index_main.run()
        return portfolio_index

    def _create_objects(self):
        self.portfolio_index_main = PortfolioMain(self.prices, self.units)

    def _get_data(self):
        self.prices, self.units = self.read_files()


if __name__ == '__main__':
    price_file = 'prices.csv'
    weights_file = 'Units.csv'
    algo = Algorithm(price_file, weights_file)
    algo.run()
