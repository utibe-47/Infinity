from exercises.Gresham.utilities import calculate_returns, calculate_statistics
from gq_data_handler import DataHandler


def get_data():
    data_handler = DataHandler()
    crypto_prices, crypto_volumes, market_prices, market_volumes = data_handler.run()
    return crypto_prices, crypto_volumes, market_prices, market_volumes


def crypto_analysis(crypto_prices):
    # Dropping crypto coins XDG Curncy, XSO Curncy, XAD Curncy, DCR1 Curncy because history of prices is below 5 years
    columns_to_drop = ['XDG Curncy', 'XSO Curncy', 'XAD Curncy', 'DCR1 Curncy']
    crypto_prices = drop_columns(crypto_prices, columns_to_drop)
    crypto_stats = calculate_statistics(crypto_prices)


def drop_columns(df, columns_to_drop):
    df.drop(columns_to_drop, inplace=True, axis=1)
    df = df.dropna(how='all')
    df = df[df.isnull().sum(axis=1) < 1]
    return df


def run():
    crypto_prices, crypto_volumes, market_prices, market_volumes = get_data()
    crypto_analysis(crypto_prices)
    crypto_returns = calculate_returns(crypto_prices)
    market_returns = calculate_returns(market_prices)


if __name__ == '__main__':
    run()