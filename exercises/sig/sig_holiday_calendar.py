from datetime import datetime
from enum import Enum

import numpy as np
import pandas as pd
from dateutil.parser import parse
from dateutil.relativedelta import MO, relativedelta
from pandas import DateOffset
from pandas._libs.tslibs.offsets import Easter, Day
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday


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


class DateHelper:

    @staticmethod
    def get_days_between_dates(from_date, to_date):
        to_date = convert_to_datetime(to_date)
        from_date = convert_to_datetime(from_date)
        num_days = (to_date - from_date).days
        return num_days

    @staticmethod
    def create_working_day_calendar(start_date=None, end_date=None):
        holiday_calendar = UkHolidaysCalendar()
        holidays = holiday_calendar.holidays().values
        if start_date is None:
            start_date = pd.to_datetime(holidays[0]).to_pydatetime()
        else:
            start_date = convert_to_datetime(start_date)

        if end_date is None:
            end_date = pd.to_datetime(holidays[-1]).to_pydatetime()
        else:
            end_date = convert_to_datetime(end_date)

        number_of_days = DateHelper.get_days_between_dates(start_date, end_date)
        working_days = [0] * number_of_days
        work_iso_days = [DayStrings.Monday.value, DayStrings.Tuesday.value, DayStrings.Wednesday.value,
                         DayStrings.Thursday.value, DayStrings.Friday.value]
        for count in np.arange(number_of_days):
            if count > 0:
                new_date = start_date + relativedelta(days=1)
            else:
                new_date = start_date
            if new_date.isoweekday() in work_iso_days and np.datetime64(new_date) not in holidays:
                working_days[count] = new_date
            start_date = new_date

        working_days = sorted(list(filter(lambda num: num != 0, working_days)))
        working_days = np.array(working_days)

        return working_days

    @staticmethod
    def get_working_days_between_dates(from_date, to_date, calendar, date_converter=None):
        if date_converter is not None:
            converter = date_converter
        else:
            converter = convert_to_datetime

        from_date = converter(from_date)
        to_date = converter(to_date)
        start_index = np.nonzero(calendar <= from_date)[0][-1]
        end_index = np.nonzero(calendar <= to_date)[0][-1]
        _dates = calendar[start_index:end_index]
        return _dates


class UkHolidaysCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('New Years Day', month=1, day=1),
        Holiday('Good Friday', month=1, day=1, offset=[Easter(), Day(-2)]),
        Holiday('Easter Monday', month=1, day=1, offset=[Easter(), Day(1)]),
        Holiday('Early May Bank Holiday', month=5, day=1, offset=DateOffset(weekday=MO(1))),
        Holiday('Spring Bank Holiday', month=5, day=31, offset=DateOffset(weekday=MO(-1))),
        Holiday('Summer Bank Holiday', month=8, day=31, offset=DateOffset(weekday=MO(-1))),
        Holiday('Christmas Day 1', month=12, day=24),
        Holiday('Christmas Day 2', month=12, day=25),
        Holiday('Christmas Day 3', month=12, day=26),
        Holiday('New Years Eve', month=12, day=31)
    ]


class DayStrings(Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7
