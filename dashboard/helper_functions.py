from os.path import join, dirname

import pandas as pd


def read_data(filename):
    folder_path = dirname(__file__)
    filepath = join(folder_path, filename)
    data = pd.read_csv(filepath)
    return data
