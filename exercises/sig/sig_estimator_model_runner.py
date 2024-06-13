import pandas as pd

from sig_contract_predictor import create_regression_model, run_analysis
from sig_datahandler import DataHandler
from sig_plotter import Plotter


class EstimationModel:

    def __init__(self):
        self.insurance_data = None
        self.position_data = None
        self.exogenous_data = None
        self.all_data = None
        self.data_reader = DataHandler()

    def run(self):
        self.run_data_handler()
        self.run_data_analysis()
        self.create_model()

    def run_data_handler(self):
        self.data_reader.run()
        self.populate_objects()

    def run_data_analysis(self):
        missing_dates = set(self.exogenous_data.index) - set(self.insurance_data.index)
        self.exogenous_data = self.exogenous_data.drop(list(missing_dates))

        columns = list(self.insurance_data.columns)
        columns.sort()
        insurance_data = self.insurance_data[columns]
        self.all_data = pd.concat([insurance_data, self.exogenous_data], axis=1)
        self.all_data.dropna(inplace=True)
        run_analysis(self.all_data)

    def visualize_input_data(self):
        Plotter.plot(self.exogenous_data, list(self.exogenous_data.columns), 'exogenous.png', save_plot=True)
        Plotter.plot_scatter(self.insurance_data, list(self.insurance_data.columns), 'insurance.png', save_plot=True)

    def create_model(self):
        mae, mse, rmse = create_regression_model(self.all_data)
        return mae, mse, rmse

    def populate_objects(self):
        self.insurance_data = self.data_reader.insurance_data
        self.position_data = self.data_reader.position_data
        self.exogenous_data = self.data_reader.exogenous_data


if __name__ == '__main__':
    runner = EstimationModel()
    runner.run()
