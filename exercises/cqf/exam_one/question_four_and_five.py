import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def run():
    percentile = 0.99
    snp_file = 'sp500_2024.csv'
    nasdaq_file = 'nasdaq100_2024.csv'
    rolling_var = {}
    ewma_var = {}
    var_span = 10
    rolling_window = 21
    factor_var = calculate_analytical_var(percentile)
    ewma_var['snp'] = run_ewma_var_analysis(snp_file, factor_var, var_span)
    ewma_var['nasdaq'] = run_ewma_var_analysis(nasdaq_file, factor_var, var_span)

    rolling_var['snp'] = run_var_analysis(snp_file, factor_var, var_span, rolling_window)
    rolling_var['nasdaq'] = run_var_analysis(nasdaq_file, factor_var, var_span, rolling_window)
    return ewma_var, rolling_var


def run_var_analysis(filename, factor_var, span, rolling_window):
    data = read_data(filename)
    data = calculate_log_return(data)
    data = calculate_log_return(data, span=span)
    data = calculate_volatility(data, rolling_window=rolling_window)
    data = calculate_var(data, factor_var, span=span)
    breach_data = data.copy(deep=True)
    breach_data = find_var_breaches(breach_data, span)
    count, percentage, breaches = calculate_breach_stats(breach_data)
    plot_var_breaches(data, breach_data)
    return count, percentage


def run_ewma_var_analysis(filename, factor_var, span):
    lamda = 0.72
    averaging_span = 252
    data = read_data(filename)
    data = calculate_log_return(data)
    data = calculate_log_return(data, span=span)
    data = calculate_ewma_vol(data, lamda, averaging_span)

    data = calculate_ewma_var(data, factor_var, span=span)
    breach_data = data.copy(deep=True)
    breach_data = find_var_breaches(breach_data, span)
    count, percentage, breaches = calculate_breach_stats(breach_data)
    plot_var_breaches(data, breach_data)
    return count, percentage


def read_data(filename):
    data = pd.read_csv(filename, parse_dates=True, index_col=0)
    return data


def calculate_log_return(data, span=1):
    returns = np.log(data['Closing Price']) - np.log(data['Closing Price'].shift(span))
    if span == 1:
        column_name = 'LogReturn'
    else:
        column_name = 'Ret_' + str(span) + 'D'
    data[column_name] = returns
    return data


def calculate_volatility(data, rolling_window=21):
    data['Vol'] = data['LogReturn'].rolling(rolling_window, min_periods=rolling_window).std()
    return data


def calculate_ewma_vol(data, lamda, averaging_span):
    data['Squared Returns'] = data['LogReturn'] ** 2
    data.dropna(inplace=True)
    data['Variance'] = np.nan
    data.iloc[0, 4] = data[:averaging_span]['Squared Returns'].mean()

    for count in range(data.shape[0]):
        if count > 0:
            data.iloc[count, 4] = (data['Variance'][count - 1] * lamda) + (
                    data['Squared Returns'][count - 1] * (1 - lamda))

    data['Vol Forecast'] = np.sqrt(data['Variance'])
    return data


def calculate_analytical_var(percentile):
    inverse_cdf = stats.norm.ppf(1 - percentile)
    return inverse_cdf


def calculate_ewma_var(data, factor_var, span=10):
    data['VaR_' + str(span) + 'D'] = data['Vol Forecast'] * np.sqrt(span) * factor_var
    return data


def calculate_var(data, factor_var, span=10):
    data['VaR_' + str(span) + 'D'] = data['Vol'] * np.sqrt(span) * factor_var
    return data


def is_breach(var, returns):
    if returns < var:
        return True
    else:
        return False


def find_var_breaches(data, span):
    var_column = 'VaR_' + str(span) + 'D'
    return_column = 'Ret_' + str(span) + 'D'
    data['Breach Indicator'] = data[[var_column, return_column]].apply(lambda x: is_breach(*x), axis=1)
    data.dropna(inplace=True)
    return data


def calculate_breach_stats(data_breaches):
    total = data_breaches.shape[0]
    breaches = data_breaches.copy(deep=True)
    breaches = breaches[breaches['Breach Indicator'] == True]
    num_breaches = breaches.shape[0]
    breach_percentage = (num_breaches / total) * 100
    return num_breaches, breach_percentage, breaches


def plot_var_breaches(data, data_breach):
    plt.rcParams.update({'font.size': 16})
    plt.title('Backtesting of Analytical VaR')
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 20
    fig_size[1] = 5
    plt.rcParams["figure.figsize"] = fig_size
    plt.plot(data.index, data['VaR_10D'], color='RED')
    plt.plot(data.index, data['Ret_10D'])
    plt.scatter(data_breach.index, data_breach['VaR_10D'], color='BLACK', marker='x')
    plt.legend(["VaR 99%/10D", "return_10D fwd", "Breach"])
    plt.grid()
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.set_title('Index Level')
    ax1.plot(data.index, data['Closing Price'])
    ax1.legend(["Index Level"])
    ax1.grid()
    plt.show()


if __name__ == '__main__':
    _ewma_var, _rolling_var = run()
