CURRENCY_TICKERS = ['GBPUSD=X', 'GBPAUD=X', 'GBPCHF=X', 'GBPJPY=X', 'GBPCAD=X', 'GBPEUR=X']
STOCK_TICKERS = ['AAPL', 'GOOG', 'MSFT', 'LLOY', 'BARC']
COMMODITY_FUTURES = ['GC=F', 'CL=F', 'NG=F', 'ZC=F', 'BZ=F', 'HE=F', 'SI=F', 'HG=F', 'LE=F', 'CC=F']
STOCK_INDICES = ['^FTSE', '^GSPC', '^DJI', '^IXIC', '^FCHI']
CRYPTO_INDICES = ['BTC-GBP', '^CMC200', 'ETH-GBP', 'SOL-GBP', 'BNB-GBP']

GTAA_TICKERS = STOCK_INDICES + STOCK_INDICES

STRATEGY_LIST = ['CommodityTrend', 'FxTrend', 'CommodityCarry', 'Gtaa', 'CryptoTrend', 'EquityValue']

STRATEGY_TICKER_DICT = {'CommodityTrend': COMMODITY_FUTURES,
                        'FxTrend': CURRENCY_TICKERS,
                        'CommodityCarry': COMMODITY_FUTURES,
                        'Gtaa': GTAA_TICKERS,
                        'EquityValue': STOCK_INDICES,
                        'CryptoTrend': CRYPTO_INDICES
                        }
