import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def run_pca(data):

    columns = list(data.columns)

    x = StandardScaler().fit_transform(data)
    pca = PCA()
    principal_components = pca.fit_transform(x)
    principal_df = pd.DataFrame(data=principal_components, columns=columns)
    var_ratio = pd.DataFrame([pca.explained_variance_ratio_], columns=columns)
    return principal_df, var_ratio


def create_regression_model(data):
    x = data[['InsuranceEU2', 'InsuranceUS1', 'InsuranceUS2', 'INTERESTRATES']]
    y = data['InsuranceEU1']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    x_train = sm.add_constant(x_train)
    x_test = sm.add_constant(x_test)

    ols_model = sm.OLS(y_train, x_train).fit()
    summary = ols_model.summary()

    # predictions = ols_model.get_prediction(x_test).summary_frame(alpha=0.05)
    predictions = ols_model.predict(x_test)

    plt.scatter(y_test, predictions)
    plt.show()

    plt.hist(y_test - predictions)
    plt.show()

    mae = metrics.mean_absolute_error(y_test, predictions)
    mse = metrics.mean_squared_error(y_test, predictions)
    rmse = np.sqrt(metrics.mean_squared_error(y_test, predictions))
    return mae, mse, rmse


def run_analysis(all_data):
    corr = all_data.corr()
    cov = all_data.cov()
    principal_df, var_ratio = run_pca(all_data)

    all_data = all_data.drop(columns=['InsuranceEU1'])
    principal_df2, var_ratio2 = run_pca(all_data)
