import numpy as np
import pandas as pd
import string


def run_weights_calculation(corr_matrix: np.ndarray) -> pd.DataFrame:
    num_assets = corr_matrix.shape[0]
    lamda = compute_lambda(num_assets, corr_matrix)
    weights = compute_weights(num_assets, corr_matrix, lamda)
    weights = weights/np.sum(weights)
    asset_names = list(string.ascii_uppercase)[:num_assets]
    portfolio_weights_df = pd.DataFrame(weights, columns=['Weights'], index=asset_names).T
    return portfolio_weights_df


def compute_lambda(num_assets: int, corr_matrix: np.ndarray) -> float:
    lamda = 1.0/np.dot(np.dot(np.ones((1, num_assets)), np.linalg.inv(corr_matrix)), np.ones((num_assets, 1)))[0][0]
    return lamda


def compute_weights(num_assets: int, corr_matrix: np.ndarray, lamda: float) -> np.array:
    weights = lamda * np.dot(np.linalg.inv(corr_matrix), np.ones((num_assets, 1)))
    return weights.flatten()


if __name__ == '__main__':
    _corr = np.array([[1, 0.4, 0.3, 0.3], [0.4, 1, 0.27, 0.5], [0.3, 0.27, 1, 0.5], [0.3, 0.42, 0.5, 1]])
    portfolio_weights = run_weights_calculation(_corr)
