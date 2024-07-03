from datetime import datetime
from sqlalchemy import desc, func, and_


def run_query(database_model, latest_orders, session):
    data = session.query(database_model).join(latest_orders, and_(
        database_model.Strategy == latest_orders.c.Strategy,
        database_model.Account == latest_orders.c.Account,
        database_model.ReasonCode == latest_orders.c.ReasonCode,
        database_model.Date == latest_orders.c.Date)).order_by(
        latest_orders.c.Date.desc(), database_model.Date.desc()).all()
    return data


def query_by_date(session, reason_code, database_model, date_limit=None):

    latest_date = session.query(database_model.Date, database_model.ReasonCode).filter(
        database_model.ReasonCode == reason_code).distinct(
        database_model.Date).order_by(desc('Date')).all()

    if date_limit is None:
        return latest_date
    else:
        latest_date = list(filter(lambda x: x[0] <= datetime.strptime(date_limit, '%Y/%m/%d'), latest_date))
    return latest_date


def query_data_by_strategy(session, database_model):
    last_orders = session.query(database_model.Strategy, func.max(database_model.Date).label(
        'latest_date')).group_by(database_model.Strategy).subquery()
    data = session.query(database_model).join(last_orders, and_(
        database_model.Strategy == last_orders.c.Strategy, database_model.Date == last_orders.c.lastest_date)).order_by(
        last_orders.c.lastest_date.desc(), database_model.Date.desc()).all()
    return data


def query_data(session, reason_code, database_model, date=None):
    if date is None:
        date_limit = func.max(database_model.Date)
        latest_orders = session.query(database_model.Date, database_model.Account,
                                      database_model.Strategy, database_model.ReasonCode).group_by(
            database_model.Account, database_model.Strategy,
            database_model.ReasonCode).having(
            and_(database_model.ReasonCode == reason_code, database_model.Date == date_limit)).subquery()
    else:
        max_date = func.max(database_model.Date)
        latest_orders = session.query(database_model.Date, database_model.Account,
                                      database_model.Strategy, database_model.ReasonCode).filter(
            database_model.Date <= date).group_by(
            database_model.Account, database_model.Strategy,
            database_model.ReasonCode).having(
            and_(database_model.ReasonCode == reason_code, database_model.Date == max_date)).subquery()

    data = run_query(database_model, latest_orders, session)

    return data


def query_latest_data(session, database_model, date_limit=None):

    if date_limit is None:
        latest_orders = session.query(database_model.Date, database_model.Account,
                                      database_model.Strategy).group_by(
            database_model.Account, database_model.Strategy).having(
            database_model.Date == func.max(database_model.Date)).subquery()
    else:
        latest_orders = session.query(database_model.Date, database_model.Account,
                                      database_model.Strategy).filter(
            database_model.Date <= date_limit).group_by(
            database_model.Account, database_model.Strategy).having(
            database_model.Date == func.max(database_model.Date)).subquery()

    data = session.query(database_model).join(latest_orders, and_(
        database_model.Strategy == latest_orders.c.Strategy,
        database_model.Account == latest_orders.c.Account,
        database_model.Date == latest_orders.c.Date)).order_by(
        latest_orders.c.Date.desc(), database_model.Date.desc()).all()

    return data


def query_latest_data_with_contract(session, database_model, date_limit=None):

    if date_limit is None:
        latest_orders = session.query(database_model.Date, database_model.Account,
                                      database_model.Strategy, database_model.Security).group_by(
            database_model.Account, database_model.Strategy, database_model.Security).having(
            database_model.Date == func.max(database_model.Date)).subquery()
    else:
        latest_orders = session.query(database_model.Date, database_model.Account,
                                      database_model.Strategy, database_model.Security).filter(
            database_model.Date >= date_limit).group_by(
            database_model.Account, database_model.Strategy, database_model.Security).having(
            database_model.Date == func.max(database_model.Date)).subquery()

    data = run_query(database_model, latest_orders, session)
    return data
