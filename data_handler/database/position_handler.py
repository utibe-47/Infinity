from datetime import datetime
from os.path import dirname
from typing import Optional

import pandas as pd

from data_handler.database.connector import sqlite_db_session
from data_handler.database.models.portfolio_position import (header, header_csv,
                                                             header_with_date, header_csv_with_date, PortfolioPositions)
from data_handler.database.queries.position_handler_queries import (query_data, query_latest_data,
                                                                    query_latest_data_with_contract)
from utilities.contract_helpers import find_latest_contract, separate_futures, find_latest_non_future_data
from utilities.datetime_helpers import DateHelpers
from utilities.decorator_functions import decorator_factory
from utilities.enums import ReasonCodes
from utilities.generic_functions import create_dataframe

DF = pd.DataFrame


def dataframe_creator(q_data):
    data = create_dataframe(q_data, *header)
    data.columns = header_csv
    return data


def dataframe_creator_with_date(q_data):
    data = create_dataframe(q_data, *header_with_date)
    data.columns = header_csv_with_date
    return data


def decorate_function(func, factory_func):
    decorator_func = decorator_factory(factory_func)
    run_time_func = decorator_func(func)
    return run_time_func


def _get_position_df(session, reason_code=None, date=None, by_security=False):
    if by_security:
        date_limit = DateHelpers.add_months(datetime.now(), -2)
        q_data = query_latest_data_with_contract(session, date_limit)
    else:
        if reason_code is not None:
            q_data = query_data(session, reason_code, date)
        else:
            if date is not None:
                q_data = query_latest_data(session, PositionHandler)
            else:
                q_data = query_latest_data(session, PositionHandler, date_limit=date)
    return q_data


def get_positions(session, strategy: Optional[str, list] = None, date: Optional[datetime] = None,
                  keep_date: bool = False):
    if strategy is None:
        latest_data = read_positions_from_db(session, date, keep_date, by_security=False)
        data = latest_data[latest_data['ReasonCode'] == ReasonCodes.rebalance.name]
    else:
        latest_data = read_positions_from_db(session, date, keep_date, by_security=True)
        latest_data = latest_data[latest_data['ReasonCode'] == ReasonCodes.rebalance.name]
        latest_data = latest_data.loc[latest_data['Strategy'].isin(strategy)]
        latest_data.reset_index(drop=True, inplace=True)
        data = process_future_data(latest_data)
    return data


def read_positions_from_db(sess, date, keep_date, by_security=False):
    if keep_date:
        run_time_func = decorate_function(_get_position_df, dataframe_creator_with_date)
        latest_data = run_time_func(sess, date=date, by_security=by_security)
    else:
        run_time_func = decorate_function(_get_position_df, dataframe_creator)
        latest_data = run_time_func(sess, date=date, by_security=by_security)
    return latest_data


def process_future_data(latest_data):
    future_data, non_future_data = separate_futures(latest_data)
    futures_list = find_latest_contract(future_data['Future/Security'].tolist())
    future_data = future_data.loc[future_data['Future/Security'].isin(futures_list)]
    non_future_data = find_latest_non_future_data(non_future_data)
    latest_data = future_data.append(non_future_data)
    latest_data.reset_index(drop=True, inplace=True)
    return latest_data


class PositionHandler:

    def __init__(self, database_name='infinity.db'):
        self.basedir = dirname(__file__)
        self.database_name = database_name

    def save_position(self, portfolio_positions: DF, run_date=None):
        if run_date is None:
            run_date = datetime.now()
        portfolio_positions.columns = header
        with sqlite_db_session(self.basedir, self.database_name) as sess:
            for index, row in portfolio_positions.iterrows():
                positions = PortfolioPositions(Date=run_date, LeadDirection=row['LeadDirection'], Lead=row['Lead'],
                                               NonLead=row['NonLead'], Security=row['Security'],
                                               PositionTarget=row['PositionTarget'], Strategy=row['Strategy'],
                                               InstrumentType=row['InstrumentType'],
                                               ReasonCode=row['ReasonCode'])

                sess.add(positions)
                sess.commit()

    def get_position(self, strategy: Optional[str, list] = None, date=None, keep_date=False):
        with sqlite_db_session(self.basedir, self.database_name) as sess:
            data = get_positions(strategy, sess, date, keep_date)
        return data


if __name__ == '__main__':
    position_handler = PositionHandler()
    _positions = position_handler.get_position()
