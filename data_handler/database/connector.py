from os.path import join
import pandas as pd
import cx_Oracle
import pyodbc
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


database_module = {'oracle': cx_Oracle, 'sql_server': pyodbc}


def create_engine(username, password, dsn, database_connector, driver):
    engine = sa.create_engine("{}+{}://{}:{}@{}".format(driver, database_connector, username, password, dsn), echo=True)
    return engine


def create_engine_sqlite(base_dir, database_name):
    engine = sa.create_engine('sqlite:///' + join(base_dir, database_name))
    return engine


@contextmanager
def db_session(username, password, dsn, database_connector, driver):
    engine = create_engine(username, password, dsn, database_connector, driver)
    session = sessionmaker()
    session.configure(bind=engine)
    sess = session()
    try:
        yield sess
    except Exception:
        raise ConnectionError('Could not connect to database')
    finally:
        sess.close()


@contextmanager
def sqlite_db_session(base_dir, database_name):
    engine = create_engine_sqlite(base_dir, database_name)
    session = sessionmaker()
    session.configure(bind=engine)
    sess = session()
    try:
        yield sess
    except Exception:
        raise ConnectionError('Could not connect to database')
    finally:
        sess.close()


def get_data(queried_data, *args):
    data_gen = ((getattr(obj_, arg) for arg in args) for obj_ in queried_data)
    data_df = pd.DataFrame(data_gen)
    data_df.columns = args
    return data_df
