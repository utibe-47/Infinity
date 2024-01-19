from dateutil.parser import parse


def refactor_headers(data):
    columns = list(data.columns)
    columns[0] = 'Date'
    data.columns = columns
    data['Date'] = data['Date'].apply(parse)
    data.set_index(columns[0], inplace=True)
    columns.pop(0)
    return data, columns


def clean_position_data(data):
    data, _ = refactor_headers(data)
    data.columns = ['Positions']
    return data


def clean_exogenous_data(data):
    data, columns = refactor_headers(data)
    data = data.fillna(method='pad')
    data.dropna(inplace=True)
    return data


def clean_insurance_data(data):
    data, columns = refactor_headers(data)
    us_contracts = list(filter(lambda x: 'US' in x, columns))
    us_data = data.copy(deep=True)
    us_data = us_data[us_contracts]
    us_data = us_data.dropna(how='all')
    eu_data = data.drop(columns=us_contracts)
    eu_data = eu_data.dropna(how='all')
    eu_data = eu_data.fillna(method='pad') if eu_data.isnull().values.any() else eu_data
    us_data = us_data.fillna(method='pad') if us_data.isnull().values.any() else us_data
    return us_data, eu_data, data
