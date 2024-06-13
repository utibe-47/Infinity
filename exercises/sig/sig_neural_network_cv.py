import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV

Parameter_Trials = {'batch_size': [10, 20, 30, 40],
                    'epochs': [10, 20, 30, 40, 50],
                    'optimizer_trial': ['adam', 'rmsprop']
                    }


def make_regression_ann(optimizer_trial):
    model = Sequential()
    model.add(Dense(units=10, input_dim=5, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(units=10, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(1, kernel_initializer='uniform'))
    model.compile(loss='mean_squared_error', optimizer=optimizer_trial)
    return model


def accuracy_score(orig, pred):
    mean_abs_percentage_error = np.mean(100 * np.abs((orig - pred) / orig))
    return 100 - mean_abs_percentage_error


def run_cross_validation(x, y):

    _model = KerasRegressor(make_regression_ann, verbose=0)
    custom_scoring = make_scorer(accuracy_score, greater_is_better=True)

    grid_search = GridSearchCV(estimator=_model,
                               param_grid=Parameter_Trials,
                               scoring=custom_scoring,
                               cv=5)

    grid_search.fit(x, y, verbose=1)
    best_params = grid_search.best_params_
    return best_params
