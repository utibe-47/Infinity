import math
import calendar as calendar_module
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from utilities.enums import DayStrings


def convert_to_datetime64(_date):
    try:
        date_ = parse(_date)
    except Exception:
        if isinstance(_date, datetime):
            date_ = np.datetime64(_date)
        elif isinstance(_date, np.datetime64):
            date_ = _date
        else:
            raise TypeError('Input date cannot be converted to datetime64. Check date type and format')
    else:
        date_ = np.datetime64(date_)
    return date_


def convert_to_datetime(_date):
    try:
        date_ = parse(_date)
    except TypeError:
        if isinstance(_date, datetime):
            date_ = _date
        elif isinstance(_date, np.datetime64):
            date_ = _date.astype(datetime)
        else:
            raise TypeError('Input date cannot be converted to datetime. Check date type and format')
    return date_


def convert_to_datetime_no_error(_date):
    try:
        date_ = parse(_date)
    except Exception:
        if isinstance(_date, datetime):
            date_ = _date
        elif isinstance(_date, np.datetime64):
            date_ = _date.astype(datetime)
        else:
            date_ = None
    return date_


def filter_calendar_by_day(_date, _day, day_strings=None):
    date = convert_to_datetime(_date)

    if day_strings is None:
        day_strings = {key: value.value for key, value in DayStrings.__members__.items()}
    day_num = day_strings[_day]
    if not hasattr(date, '__len__'):
        date = list(date)
    dates = np.array(list(filter(lambda dd: dd.isoweekday() == day_num, date)))
    indices = np.where(np.in1d(_date, dates))[0]
    return indices


def year(dates):
    """Return an array of the years given an array of datetime64s"""
    return dates.astype('M8[Y]').astype('i8') + 1970


def month(dates):
    """Return an array of the months given an array of datetime64s"""
    return dates.astype('M8[M]').astype('i8') % 12 + 1


def day(dates):
    """Return an array of the days of the month given an array of datetime64s"""
    return (dates - dates.astype('M8[M]')) / np.timedelta64(1, 'D') + 1


def date_to_datetime(_date):
    dt = datetime.combine(_date.today(), datetime.min.time())
    return dt


# Need to unit test this to make sure it can handle an array of dates 16-09-2019
def get_number_of_years(end_date, start_date, days_in_year=365):
    try:
        time_diff = (end_date - start_date).astype('timedelta64[D]')
    except TypeError:
        end_date = convert_to_datetime64(end_date)
        start_date = convert_to_datetime64(start_date)
        try:
            time_diff = (end_date - start_date).astype('timedelta64[D]')
        except (RuntimeError, TypeError):
            raise NotImplemented('Could not execute time difference calculation')
    num_days = time_diff / np.timedelta64(1, 'D')
    num_years = num_days / days_in_year
    return num_years


def get_number_of_months(end_date, start_date) -> float:
    if isinstance(start_date, np.datetime64):
        start_date = start_date.astype(datetime)
    try:
        num_months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
    except TypeError:
        end_date = convert_to_datetime(end_date)
        start_date = convert_to_datetime(start_date)
        try:
            num_months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
        except TypeError:
            raise TypeError('Cannot find number of months, ensure that datetime inputs are used')
    return num_months


def get_nearest_preceding_working_day(start_date, calendar, date_formatter=convert_to_datetime):
    index = np.nonzero(calendar <= convert_to_datetime(start_date))[0][-1]
    _new_date = calendar[index]
    return date_formatter(_new_date)


def get_last_working_day_of_month(calendar, interval=0, date_formatter=convert_to_datetime):
    # _calendar = list(map(convert_to_datetime, calendar))
    last_day = []

    def last_day_of_month(_date):
        _year = _date.year
        _month = _date.month
        _, day_ = calendar_module.monthrange(_year, _month)
        _last_day = get_nearest_preceding_working_day(_date.replace(day=day_), calendar)
        return _last_day

    for _day in calendar:
        if len(last_day) > 0:
            if _day not in last_day and np.abs(get_number_of_months(_day, last_day[len(last_day) - 1])) > interval:
                if date_formatter is None:
                    last_day.append(last_day_of_month(_day))
                else:
                    last_day.append(date_formatter(last_day_of_month(_day)))
        else:
            if date_formatter is None:
                last_day.append(last_day_of_month(_day))
            else:
                last_day.append(date_formatter(last_day_of_month(_day)))

    last_day = sorted(list(set(last_day)))
    return np.array(last_day)


def get_whole_number_of_months(end_date, start_date):
    yrs = get_number_of_years(end_date, start_date)
    num_months = math.floor(yrs * 12)
    return num_months


def get_minimum_date():
    return np.datetime64('1678-02-17T16:53:25')


class DateHelpers:

    @staticmethod
    def add_working_days(from_date, num_days, calendar):
        from_date = convert_to_datetime(from_date)
        index = np.nonzero(calendar <= from_date)[0][-1]
        new_index = index + num_days
        return calendar[new_index]

    @staticmethod
    def get_working_days_between_dates(from_date, to_date, calendar, converter=None):
        if converter is not None:
            from_date = converter(from_date)
            to_date = converter(to_date)
        start_index = np.nonzero(calendar <= from_date)[0][-1]
        end_index = np.nonzero(calendar <= to_date)[0][-1]
        _dates = calendar[start_index:end_index]
        return _dates

    @staticmethod
    def get_number_of_working_days(from_date, to_date, calendar, converter=None):
        dates = DateHelpers.get_working_days_between_dates(from_date, to_date, calendar, converter)
        return len(dates)

    @staticmethod
    def get_days_between_dates(from_date, to_date):
        to_date = convert_to_datetime(to_date)
        from_date = convert_to_datetime(from_date)
        num_days = (from_date - to_date).days
        return num_days

    @staticmethod
    def change_date_str_fmt(date_str):
        date_ = parse(date_str)
        return date_.strftime('%d-%b-%Y')

    @staticmethod
    def convert_dt_to_str(date, date_format='%Y-%m-%d'):
        try:
            date_dt = parse(date)
        except TypeError:
            if isinstance(date, datetime):
                date_dt = date
            elif isinstance(date, np.datetime64):
                date_dt = date.astype(datetime)
            else:
                raise TypeError('Input date needs to be either a valid date string, datetime or datetime64 object')
        return datetime.strftime(date_dt, date_format)

    @staticmethod
    def convert_datetime64d_to_str(_date, date_format):
        dt = pd.to_datetime(_date)
        date_str = dt.strftime(date_format)
        return date_str

    @staticmethod
    def change_date_str(_date):
        date_ = parse(_date)
        return date_.strftime('%Y-%m-%d')

    @staticmethod
    def convert_str_datetime(date_str):
        _date = parse(date_str)
        return _date

    @staticmethod
    def convert_str_full_datetime(date_str):
        _date = parse(date_str)
        dt_now = datetime.now()
        full_date = _date + timedelta(hours=dt_now.hour, minutes=dt_now.minute, seconds=dt_now.second,
                                      microseconds=dt_now.microsecond)
        return full_date

    @staticmethod
    def convert_str_datetime64(date_str):
        _date = np.datetime64(date_str)
        return _date

    @staticmethod
    def add_months(_date, n_months, format_converter=convert_to_datetime):
        date_ = DateHelpers._parse_date(_date)
        new_date = date_ + relativedelta(months=n_months)
        return new_date if format_converter is None else format_converter(new_date)

    @staticmethod
    def _parse_date(_date):
        try:
            date_ = parse(_date)
        except TypeError:
            if isinstance(_date, datetime):
                date_ = _date
            elif isinstance(_date, np.datetime64):
                date_ = _date.astype(datetime)
            else:
                raise TypeError('Input date in the wrong format')
        return date_

    @staticmethod
    def add_days(_date, n_days, format_converter=convert_to_datetime):
        date_ = DateHelpers._parse_date(_date)
        new_date = date_ + relativedelta(days=n_days)
        return new_date if format_converter is None else format_converter(new_date)

    @staticmethod
    def add_years(_date, n_years, format_converter=convert_to_datetime64):
        date_ = DateHelpers._parse_date(_date)
        new_date = date_ + relativedelta(years=n_years)
        return new_date if format_converter is None else format_converter(new_date)

    @staticmethod
    def get_first_of_month(_date, format_converter=convert_to_datetime64):
        date_ = DateHelpers._parse_date(_date)
        date_beta = date_ + relativedelta(day=1)
        return format_converter(date_beta)
