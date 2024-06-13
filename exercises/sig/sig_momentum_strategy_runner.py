from sig_datahandler import DataHandler
from sig_plotter import Plotter
from sig_signal_estimator import check_signal_correlation, create_signal_prediction_model, estimate_portfolio
from sig_signal_processor import decompose_signal, unit_root_test
from sig_span_optimization import run_optimization


class MomentumStrategyModelRunner:

    def __init__(self):
        self.us_insurance_data = None
        self.eu_insurance_data = None
        self.position_data = None
        self.predictors = None
        self.data_reader = DataHandler()

    def run(self):
        self.run_data_handler()
        self.populate_objects()
        self.visualize_input_data()
        self.analyse_input_data()
        _, signals = self.check_all_span_signal_corr(create_heatmap=False)
        self.optimize_span()
        self.create_signal_prediction_model()

    def run_data_handler(self):
        self.data_reader.run()

    def visualize_input_data(self):
        Plotter.plot(self.eu_insurance_data, ['InsuranceEU1'], 'InsuranceEU1', save_plot=True)
        Plotter.plot_scatter(self.position_data, ['Positions'], 'Portfolio_positions', save_plot=True)
        position_change = self.position_data.diff(periods=1)
        Plotter.plot_scatter(position_change, ['Positions'], 'position_changes', save_plot=True)

    def analyse_input_data(self):
        insurance_eu1 = self.eu_insurance_data[['InsuranceEU1']]
        decompose_signal(insurance_eu1)
        unit_root_test(insurance_eu1.values)

    def check_all_span_signal_corr(self, create_heatmap=False):
        insurance_eu1 = self.eu_insurance_data[['InsuranceEU1']]
        corr, signal_combinations = check_signal_correlation(insurance_eu1, create_heatmap=create_heatmap)
        return corr, signal_combinations

    def optimize_span(self):
        insurance_eu1 = self.eu_insurance_data[['InsuranceEU1']]
        self.predictors = run_optimization(insurance_eu1, self.position_data)

    def create_signal_prediction_model(self):
        insurance_eu1 = self.eu_insurance_data[['InsuranceEU1']]
        span_data = [5, 250, 45]
        model, model_accuracy, testing_data = create_signal_prediction_model(insurance_eu1, self.position_data,
                                                                             self.predictors, *span_data)
        portfolio = estimate_portfolio(model, insurance_eu1)
        Plotter.plot(portfolio, ['Positions'], 'estimated_portfolio.png', save_plot=True)

    def populate_objects(self):
        self.us_insurance_data = self.data_reader.us_insurance_data
        self.eu_insurance_data = self.data_reader.eu_insurance_data
        self.position_data = self.data_reader.position_data


if __name__ == '__main__':
    runner = MomentumStrategyModelRunner()
    runner.run()
