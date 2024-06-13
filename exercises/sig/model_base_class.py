from sig_datahandler import DataHandler


class BaseClass:

    def __init__(self):
        self.us_insurance_data = None
        self.eu_insurance_data = None
        self.position_data = None
        self.exogenous_data = None
        self.data_reader = DataHandler()

    def run_data_handler(self):
        self.data_reader.run()

    def populate_objects(self):
        self.us_insurance_data = self.data_reader.us_insurance_data
        self.eu_insurance_data = self.data_reader.eu_insurance_data
        self.position_data = self.data_reader.position_data
        self.exogenous_data = self.data_reader.exogenous_data
