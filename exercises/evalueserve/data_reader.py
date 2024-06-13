import logging
from os.path import dirname, abspath, join

import pandas as pd


class DataReader:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def read_csv_pd(self, filename, is_full_file_path=False, folder_path=None, **kwargs):
        filename = self.get_full_filename(filename, folder_path, is_full_file_path)
        try:
            csv_data = pd.read_csv(filename, **kwargs)
        except Exception as e:
            msg = 'Could not read csv file: {}, exception {} was raised'.format(filename, str(e))
            raise Exception(msg)
        return csv_data

    def get_full_filename(self, filename, folder_path, isfile_path):
        if not isfile_path:
            if folder_path is None:
                filename = self._get_filepath(filename)
            else:
                filename = join(folder_path, filename)
        return filename

    def _get_filepath(self, filename):
        try:
            directory_name = dirname(abspath(__file__))
        except FileNotFoundError:
            raise FileNotFoundError('Could not find file {}, confirm that file exists in same directory as '
                                    '{} class'.format(filename, self.__name__))
        else:
            return join(directory_name, filename)
