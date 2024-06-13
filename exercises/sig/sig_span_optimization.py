import numpy as np
from itertools import combinations

from sig_neural_network import run_nn_model
from sig_utilities import create_span_combinations, create_signal_combinations, compile_dataset


def run_optimization(data, position_data):
    min_span, max_span, span_step = (5, 250, 45)
    span_combinations = create_span_combinations(min_span, max_span, span_step)
    signals = create_signal_combinations(data, span_combinations)
    dataset = compile_dataset(position_data, signals)
    signal_list = list(dataset.columns)[1:]
    signal_combinations = combinations(signal_list, 5)

    errors = []
    _combinations = []
    for comb in signal_combinations:
        predictors = list(comb)
        target_variable = ['Positions']
        model, testing_data = run_nn_model(dataset, target_variable, predictors)

        abs_percent_error = 100 * abs(
            (testing_data['PredictedPositions'] - testing_data['OriginalPositions']) / testing_data[
                'OriginalPositions'])
        model_accuracy = 100 - np.mean(abs_percent_error)
        errors.append(model_accuracy)
        _combinations.append(predictors)

    index_max = np.argmax(np.array(errors))
    best_predictor = _combinations[index_max]
    return best_predictor
