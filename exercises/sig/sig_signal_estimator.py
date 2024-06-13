import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd

from sig_neural_network import run_nn_model
from sig_utilities import create_span_combinations, ewma_cross, create_signal_combinations, compile_dataset

crossed_dict = {'ewma_1_50': [1, 50], 'ewma_20_100': [20, 100], 'ewma_50_210': [50, 210]}


def compute_signal(weights, *ewma_crosses):
    combined_cross = pd.concat(ewma_crosses, axis=1)
    cross_list = list(combined_cross.columns)
    weight_dict = dict(zip(cross_list, weights))
    _signal = combined_cross.mul(weight_dict).sum(axis=1)
    return _signal


def generate_signal(contract_trading_volume, weights):

    crosses = []
    for key, values in crossed_dict.items():
        short, long = values
        crosses.append(ewma_cross(contract_trading_volume, short, long, header=key))
    signal = compute_signal(weights, *crosses)
    return signal


def check_signal_correlation(data, create_heatmap=True):
    min_span, max_span, span_step = (5, 250, 45)
    _combinations = create_span_combinations(min_span, max_span, span_step)
    signals = create_signal_combinations(data, _combinations)
    signal_corr = signals.corr()
    if create_heatmap:
        sns.heatmap(signal_corr, cmap="tab20", annot=True)
        plt.savefig('heatmap.png')
        plt.show()
    return signal_corr, signals


def create_signal_prediction_model(data, position_data, predictors, min_span, max_span, span_step):
    _combinations = create_span_combinations(min_span, max_span, span_step)
    signals = create_signal_combinations(data, _combinations)
    dataset = compile_dataset(position_data, signals)

    target_variable = ['Positions']
    model, testing_data = run_nn_model(dataset, target_variable, predictors)

    abs_percent_error = 100 * abs((testing_data['PredictedPositions'] - testing_data['OriginalPositions']) / testing_data['OriginalPositions'])
    testing_data['AbsolutePercentageError'] = abs_percent_error
    model_accuracy = 100 - np.mean(abs_percent_error)
    testing_data.head()
    return model, model_accuracy, testing_data


def estimate_portfolio(model, data):
    pass
