import warnings
import pandas as pd
import numpy as np
from pprint import pprint
from collections import OrderedDict
from numpy.linalg import multi_dot
from scipy import stats
from tabulate import tabulate
from sqlalchemy import create_engine, text

import plotly.express as px

warnings.filterwarnings('ignore')
px.defaults.width, px.defaults.height = 1000, 600

# Set precision
pd.set_option('display.precision', 4)


assets = sorted(['ICICIBANK', 'ITC', 'RELIANCE', 'TCS', 'ASIANPAINT'])

df = pd.DataFrame()

engine = create_engine('sqlite:///Nifty50')

for asset in assets:
    query = f'SELECT Date, Close FROM  {asset}'
    with engine.connect() as connection:
        df1 = pd.read_sql_query(text(query), connection, index_col='Date')
        df1.columns = [asset]
    df = pd.concat([df, df1], axis=1)


returns = df.pct_change().dropna()

stockreturn = returns['ICICIBANK']

mean = np.mean(stockreturn)
stdev = np.std(stockreturn)

VaR_90 = stats.norm.ppf(1-0.90, mean, stdev)
VaR_95 = stats.norm.ppf(1-0.95, mean, stdev)
VaR_99 = stats.norm.ppf(1-0.99, mean, stdev)


table = [['90%', VaR_90],['95%', VaR_95],['99%', VaR_99] ]
header = ['Confidence Level', 'Value At Risk']
print(tabulate(table,headers=header))


# Use quantile function for Historical VaR
hVaR_90 = returns['ICICIBANK'].quantile(0.10)
hVaR_95 = returns['ICICIBANK'].quantile(0.05)
hVaR_99 = returns['ICICIBANK'].quantile(0.01)

# Ouput results in tabular format
htable = [['90%', hVaR_90],['95%', hVaR_95],['99%', hVaR_99]]
print(tabulate(htable,headers=header))

# Set seed for reproducibility
np.random.seed(42)

# Number of simulations
n_sims = 5000

# Simulate returns and sort
sim_returns = np.random.normal(mean, stdev, n_sims)

# Use percentile function for MCVaR
MCVaR_90 = np.percentile(sim_returns,10)
MCVaR_95 = np.percentile(sim_returns, 5)
MCVaR_99 = np.percentile(sim_returns,1)