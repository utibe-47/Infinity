import string

import numpy as np
import pandas as pd


def run_stressed_cases(stress_factors: list[float], return_target: float, mew: np.ndarray, corr_matrix: np.ndarray):
    portfolio_risks, portfolio_weights = [], []
    num_assets = corr_matrix.shape[0]
    asset_names = list(string.ascii_uppercase)[:num_assets]
    correlation_matrix = {}
    for factor in stress_factors:
        corr = compute_stressed_matrix(num_assets, factor, corr_matrix)
        weights, portfolio_risk = calculate_portfolio_metrics(return_target, num_assets, mew, corr)
        portfolio_weights.append(weights.flatten())
        portfolio_risks.append(portfolio_risk)
        correlation_matrix[factor] = pd.DataFrame(corr, columns=asset_names, index=asset_names)

    weights_df = pd.DataFrame(np.row_stack(portfolio_weights), columns=asset_names, index=stress_factors).T
    risks_df = pd.DataFrame(portfolio_risks, columns=['Volatility'], index=stress_factors).T
    return weights_df, risks_df


def calculate_portfolio_metrics(return_target: float, num_assets: int, mew: np.ndarray, corr_matrix: np.ndarray):

    a, b, c = compute_factors(num_assets, mew, corr_matrix)
    lamda = compute_lambda(a, b, c, return_target)
    gamma = compute_gamma(a, b, c, return_target)
    weights = compute_weights(num_assets, mew, corr_matrix, lamda, gamma)
    weights = weights/np.sum(weights)
    portfolio_risk = calculate_risk(weights, corr_matrix)
    return weights, portfolio_risk


def compute_lambda(a: float, b: float, c: float, m: float) -> float:
    lamda = ((a * m) - b) / ((a * c) - (b ** 2))
    return lamda


def compute_gamma(a: float, b: float, c: float, m: float) -> float:
    gamma = (c - (b * m))/((a*c) - (b ** 2))
    return gamma


def compute_factors(num_assets: int, mew: np.ndarray, corr_matrix: np.ndarray) -> tuple[float, float, float]:
    a = np.dot(np.dot(np.ones((1, num_assets)), np.linalg.inv(corr_matrix)), np.ones((num_assets, 1)))[0][0]
    b = np.dot(np.dot(np.transpose(mew), np.linalg.inv(corr_matrix)), np.ones((num_assets, 1)))[0][0]
    c = np.dot(np.dot(np.transpose(mew), np.linalg.inv(corr_matrix)), mew)[0][0]
    return a, b, c


def compute_weights(num_assets: int, mew: np.ndarray, corr_mat: np.ndarray, lamda: float, gamma: float) -> np.ndarray:
    weights = np.dot(np.linalg.inv(corr_mat), ((lamda * mew) + (gamma * np.ones((num_assets, 1)))))
    return weights


def calculate_risk(weights: np.ndarray, corr: np.ndarray) -> float:
    risk = np.sqrt(np.dot(np.dot(np.transpose(weights), corr), weights))[0][0]
    return risk


def compute_stressed_matrix(num_assets: int, factor: float, corr_matrix: np.ndarray) -> np.ndarray:
    limits = np.diag(np.full(num_assets, 1.0))
    _limits = np.where(limits == 0, 0.99, limits)

    corr_matrix = corr_matrix * factor
    corr_matrix = np.clip(corr_matrix, a_max=_limits, a_min=0, out=corr_matrix)
    return corr_matrix


if __name__ == '__main__':
    target = 0.07
    _factors = [1, 1.3, 1.8]
    _mew = np.array([0.05, 0.07, 0.15, 0.22])
    _mew = _mew[:, None]
    _corr = np.array([[1, 0.4, 0.3, 0.3], [0.4, 1, 0.27, 0.5], [0.3, 0.27, 1, 0.5], [0.3, 0.42, 0.5, 1]])
    portfolio_weights_df, portfolio_risks_df = run_stressed_cases(_factors, target, _mew, _corr)
