import json
import pandas as pd


def parse_data(data):
    _data = pd.json_normalize(json.loads(data))
    return _data


