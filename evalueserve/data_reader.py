import csv
import logging
from os.path import dirname, abspath, join

import pandas as pd

from utilities import return_dataframe, return_dataframe_with_dt


class DataReader:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def read_csv_pd(filename, **kwargs):
        try:
            csv_data = pd.read_csv(filename, **kwargs)
        except Exception as e:
            msg = 'Could not read csv file: {}, exception {} was raised'.format(filename, str(e))
            raise Exception(msg)
        return csv_data

    @return_dataframe
    def read_csv(self, filename, folder_path=None, isfile_path=True):
        return self._read_csv(filename, folder_path, isfile_path)

    @return_dataframe_with_dt
    def read_csv_with_dt(self, filename, folder_path=None, isfile_path=True):
        return self._read_csv(filename, folder_path, isfile_path)

    def _read_csv(self, filename, folder_path=None, isfile_path=True):
        if not isfile_path:
            if folder_path is None:
                filename = self._get_filepath(filename)
            else:
                filename = join(folder_path, filename)
        csv_data = []
        try:
            with open(filename, newline='') as csvfile:
                csv_reader = csv.reader(csvfile, dialect="excel")
                for row in csv_reader:
                    csv_data.append(row)
        except FileNotFoundError:
            self.logger.debug('Could not find file {}'.format(filename))
            raise FileNotFoundError('Could not find file {}, confirm that file exists in same directory as '
                                    '{} class'.format(filename, DataReader.__name__))
        return csv_data

    def _get_filepath(self, filename):
        try:
            directory_name = dirname(abspath(__file__))
        except FileNotFoundError:
            raise FileNotFoundError('Could not find file {}, confirm that file exists in same directory as '
                                    '{} class'.format(filename, self.__name__))
        else:
            return join(directory_name, filename)

    def file_types_handled(self):
        return {'.csv': self.read_csv, '.txt': self.read_text_file, '.xlsx': self.read_excel,
                '.xlsb': self.read_excel_binary}
