import pandas as pd


class ExcelDataReader:

    def read(self, fullpath, date_parser=None, parse_dates=None, rows_skipped=None, sheet_name=None):
        excel_data = self.read_excel(fullpath, date_parser, parse_dates, rows_skipped, sheet_name)
        return excel_data

    @staticmethod
    def read_excel(filename, date_parser, parse_dates, rows_skipped, sheet_name, **kwargs):
        try:
            excel_data = pd.read_excel(filename, sheet_name=sheet_name, skiprows=rows_skipped,
                                       parse_dates=parse_dates, date_parser=date_parser, **kwargs)
        except Exception as e:
            msg = 'Could not read excel spreadsheet with filename: {}, exception {} was raised'.format(filename, str(e))
            raise Exception(msg)
        return excel_data
