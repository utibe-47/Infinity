import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sig_neural_network_cv import run_cross_validation, make_regression_ann


def split_data(data, target_variable, predictors):

    x = data[predictors].values
    y = data[target_variable].values

    predictor_scaler = StandardScaler()
    target_scaler = StandardScaler()

    predictor_scaler_fit = predictor_scaler.fit(x)
    target_var_scaler_fit = target_scaler.fit(y)

    x = predictor_scaler_fit.transform(x)
    y = target_var_scaler_fit.transform(y)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
    return x_train, x_test, y_train, y_test, predictor_scaler_fit, target_var_scaler_fit


def generate_predictions(model, predictor_scaler_fit, target_var_scaler_fit, predictors, x_test, y_test):

    predictions = model.predict(x_test)
    predictions = target_var_scaler_fit.inverse_transform(predictions)
    y_test_orig = target_var_scaler_fit.inverse_transform(y_test)
    test_data = predictor_scaler_fit.inverse_transform(x_test)

    testing_data = pd.DataFrame(data=test_data, columns=predictors)
    testing_data['OriginalPositions'] = y_test_orig
    testing_data['PredictedPositions'] = predictions
    testing_data.head()
    return testing_data


def run_nn_model(data, target_variable, predictors):
    x_train, x_test, y_train, y_test, predictor_scaler_fit, target_var_scaler_fit = split_data(data, target_variable, predictors)
    best_params = run_cross_validation(x_train, y_train)
    model = make_regression_ann(best_params['optimizer_trial'])
    model.fit(x_train, y_train, batch_size=best_params['batch_size'], epochs=best_params['epochs'], verbose=1)
    testing_data = generate_predictions(model, predictor_scaler_fit, target_var_scaler_fit, predictors, x_test, y_test)
    return model, testing_data


def vec_impl(df):
    import datetime
    cutoff_date = datetime.date.today() + datetime.timedelta(days=2)
    output = (2*(df['priority'] == 'HIGH') + (df['due_date'] <= cutoff_date))
    return output
