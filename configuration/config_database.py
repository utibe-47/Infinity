import os
from os.path import join, dirname
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib
from urllib import parse

BASEDIR = os.path.dirname(os.path.dirname(__file__))
BASEDIR_RESULTS = os.path.join(BASEDIR, 'results')

# DB Settings
DRIVER = '{SQL Server};'
DB_SERVER = 'ldnec1bp\gtps'

DB_DATABASE = 'quant_risk_it'
GAM_DATABASE = 'find'
TRUSTED_CONNECTION = 'yes;'

params = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=ldnec1bp\gtps;DATABASE=quant_risk_it;Trusted_Connection=yes")
params_aum = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=ldnec1bp\gtps;DATABASE=find;Trusted_Connection=yes")
data_engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)


def data_engine_aum():
    return create_engine("mssql+pyodbc:///?odbc_connect=%s" % params_aum)


application_engine = create_engine("sqlite:///%s/app.db" % BASEDIR)

# DB Sessions
DataSession = sessionmaker(bind=data_engine)
AumDataSession = sessionmaker(bind=data_engine_aum())
ApplicationSession = sessionmaker(bind=application_engine)
Session = ApplicationSession()

# DB Declarative Bases
DataBase = declarative_base(bind=data_engine)
AumDataBase = declarative_base(bind=data_engine_aum())
ApplicationBase = declarative_base(bind=application_engine)
