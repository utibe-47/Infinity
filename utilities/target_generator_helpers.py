from typing import Dict

import numpy as np
import pandas as pd

from data_handler.tickers import STRATEGY_TICKER_DICT, STRATEGY_LIST
from utilities.enums import LeadDirection
from utilities.generic_functions import clean_ticker


def get_signals() -> Dict[str, pd.DataFrame]:
    signal_dict = {}
    for strategy, ticker_list in STRATEGY_TICKER_DICT.items():
        if strategy in ['Gtaa', 'FxTrend']:
            signal = np.random.random(size=len(ticker_list))
        else:
            signal = np.zeros(shape=len(ticker_list), dtype=float)
            for ind in range(len(ticker_list)):
                num = np.random.uniform(-1, 1)
                if num > 0.7:
                    num = 0.7
                if num < -0.7:
                    num = -0.7
                signal[ind] = num

        signals = signal / np.abs(signal.sum())
        ticker_list = list(map(clean_ticker, ticker_list))
        signals = pd.DataFrame(signals, index=ticker_list, columns=['Signal']).reset_index(names=['Ticker'])
        signal_dict[strategy] = signals
    return signal_dict


def get_allocations() -> pd.DataFrame:
    allocations = np.random.random(size=len(STRATEGY_LIST))
    allocations = allocations / allocations.sum()
    allocations = pd.DataFrame(allocations, index=STRATEGY_LIST, columns=['Weight']).reset_index(names=['Strategy'])
    return allocations


def get_aum():
    aum = 1000000
    return aum


def check_trade_direction(target):
    if target < 0:
        direction = LeadDirection.Sell.name
    elif target == 0:
        direction = LeadDirection.Hold.name
    else:
        direction = LeadDirection.Buy.name
    return direction
