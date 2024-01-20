from evalueserve.Descriptors.meta_helpers import DescriptorNamingMeta
from evalueserve.data_reader import DataReader


class Algorithm(metaclass=DescriptorNamingMeta):

    def __init__(self, pricing_filename, weights_filename):
        self.pricing_file = pricing_filename
        self.weights_file = weights_filename
        self.data_reader = DataReader()

    def read_files(self):
        pricing_data = self.data_reader.read(self.pricing_file, isfile_path=False, folder_path=None)
        pricing_data = self.data_reader.read(self.pricing_file, isfile_path=False, folder_path=None)

