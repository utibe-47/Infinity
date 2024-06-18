from os.path import dirname, abspath, join, isfile
from os import listdir
import csv
import pandas as pd
import logging
import pathlib
import xlrd

from utilities.decorator_functions import return_dataframe, return_dataframe_with_dt


class DataReader:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def read(self, file_name, **kwargs):
        file_ext = pathlib.Path(file_name).suffix
        try:
            func = self.file_types_handled()[file_ext]
        except KeyError:
            output_data = self.read_text_file(file_name, **kwargs)
        else:
            output_data = func(file_name, **kwargs)

        return output_data

    def read_excel(self, filename, folder_path=None, isfile_path=True, sheet_name=None, rows_skipped=None,
                   parse_dates=False, date_parser=None, **kwargs):

        if isfile_path:
            if folder_path is None:
                filename = self._get_filepath(filename)
            else:
                filename = join(folder_path, filename)

            sheet_name = self._get_sheet_name(filename, sheet_name)
            excel_data = self._read_excel(filename, date_parser, parse_dates, rows_skipped, sheet_name, **kwargs)
            return excel_data
        else:
            filepath = self._get_filepath(filename)
            sheet_name = self._get_sheet_name(filename, sheet_name)
            return self._read_excel(filepath, date_parser, parse_dates, rows_skipped, sheet_name)

    def read_excel_binary(self, filename, folder_path=None, isfile_path=True, **kwargs):

        if isfile_path:
            if folder_path is None:
                filename = self._get_filepath(filename)
            else:
                filename = join(folder_path, filename)

            excel_data = pd.read_excel(filename, **kwargs)
            return excel_data
        else:
            filepath = self._get_filepath(filename)
            return pd.read_excel(filepath, **kwargs)

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

    @staticmethod
    def _read_excel(filename, date_parser, parse_dates, rows_skipped, sheet_name, **kwargs):
        try:
            excel_data = pd.read_excel(filename, sheet_name=sheet_name, skiprows=rows_skipped,
                                       parse_dates=parse_dates, date_parser=date_parser, **kwargs)
        except Exception as e:
            msg = 'Could not read excel spreadsheet with filename: {}, exception {} was raised'.format(filename, str(e))
            raise Exception(msg)
        return excel_data

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

    def read_text_file(self, filename, folder_path=None, isfile_path=True):
        if not isfile_path:
            if folder_path is None:
                filename = self._get_filepath(filename)
            else:
                filename = join(folder_path, filename)
        try:
            text_data = pd.read_fwf(filename)
        except Exception as e:
            raise Exception('Could not read file with exception: {} raised'.format(str(e)))
        return text_data

    def _get_filepath(self, filename):
        try:
            directory_name = dirname(abspath(__file__))
        except FileNotFoundError:
            raise FileNotFoundError('Could not find file {}, confirm that file exists in same directory as '
                                    '{} class'.format(filename, self.__name__))
        else:
            return join(directory_name, filename)

    def _get_filepath_with_folder(self, filename, folder_name):
        try:
            dir_path = abspath(folder_name)
        except NotADirectoryError:
            raise NotADirectoryError('Could not find folder {}, confirm that folder exists in same '
                                     'directory as {} class'.format(folder_name, self.__name__))
        else:
            return join(dir_path, filename)

    def file_types_handled(self):
        return {'.csv': self.read_csv, '.txt': self.read_text_file, '.xlsx': self.read_excel,
                '.xlsb': self.read_excel_binary}

    @staticmethod
    def get_filenames(folder_path):
        files = [file for file in listdir(folder_path) if isfile(join(folder_path, file))]
        return files

    @staticmethod
    def _get_sheet_name(filepath, sheet_name):
        if sheet_name is None:
            try:
                xls = xlrd.open_workbook(filepath, on_demand=True)
                sheet_names = xls.sheet_names()
                sheet_name = ''
                for _name in sheet_names:
                    nrows = xls.sheet_by_name(_name).nrows
                    if nrows > 0:
                        sheet_name = _name
                        break
                if bool(sheet_name):
                    return sheet_name
                else:
                    raise Exception('Excel spreadsheet is empty')
            except Exception as e:
                msg = 'Could not read excel spreadsheet with filepath: {}, exception {} was ' \
                      'raised'.format(filepath, str(e))
                raise Exception(msg)
        else:
            return sheet_name
