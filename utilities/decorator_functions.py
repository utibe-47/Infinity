import functools

from datetime import datetime
from functools import partial, wraps
import time
import pandas as pd
from dateutil.parser import parse

from utilities.datetime_helpers import convert_to_datetime_no_error


def timer(func):
    """Print the runtime of the decorated function"""
    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(" Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer


def change_df_index_date_func(array):
    array = list(map(partial(change_date_str, format_string='%d/%m/%Y'), list(array)))
    array = pd.to_datetime(array, format='%d/%m/%Y')
    return array


def return_dataframe(func):
    @wraps(func)
    def wrapper_(*args, **kwargs):
        value = func(*args, **kwargs)
        result = pd.DataFrame(value[1:])
        result.columns = value[0]
        result.set_index(value[0][0], inplace=True)
        try:
            result[result.columns] = result[result.columns].apply(pd.to_numeric, errors='coerce', raw=False)
        except Exception:
            for index, row in result.iterrows():
                result.loc[index] = pd.to_numeric(row)
        if all(isinstance(val, datetime) or isinstance(convert_to_datetime_no_error(val), datetime) for val in result.index):
            result.index = change_df_index_date_func(result.index)
        return result
    return wrapper_


def return_dataframe_without_dt(func):
    @wraps(func)
    def wrapper_(*args, **kwargs):
        value = func(*args, **kwargs)
        result = pd.DataFrame(value[1:])
        result.columns = value[0]
        result.set_index(value[0][0], inplace=True)
        try:
            result[result.columns] = result[result.columns].apply(pd.to_numeric, errors='coerce', raw=False)
        except ValueError:
            for index, row in result.iterrows():
                result.loc[index] = pd.to_numeric(row)
        result.index = change_df_index_date_func(result.index)
        return result
    return wrapper_


def return_dataframe_with_dt(func):
    @wraps(func)
    def wrapper_(*args, **kwargs):
        value = func(*args, **kwargs)
        result = pd.DataFrame(value[1:])
        result.columns = value[0]
        try:
            result[result.columns[1:]] = result[result.columns[1:]].apply(pd.to_numeric, errors='coerce', raw=False)
        except ValueError:
            for index, row in result.iterrows():
                result.loc[index] = pd.to_numeric(row)
        result.iloc[:, 0] = change_df_index_date_func(result.iloc[:, 0])
        return result
    return wrapper_


def change_df_index_date(func):
    @wraps(func)
    def wrapper_converter(*args, **kwargs):
        value = func(*args, **kwargs)
        value.index = pd.to_datetime(value.index, format='%d/%m/%Y')
        # value.index = list(map(partial(change_date_str, format_string='%d/%m/%Y'), list(value.index)))
        return value
    return wrapper_converter()


def change_date_str(_date, format_string='%d/%m/%Y'):
    date_ = parse(_date)
    return date_.strftime(format_string)


def decorator_factory(processing_func):
    def decorator(func):
        @wraps(func)
        def wrapper_timer(*args, **kwargs):
            value = func(*args, **kwargs)
            processed_value = processing_func(value)
            return processed_value
        return wrapper_timer
    return decorator


def decorator_with_param_check(obj, names):
    def decorator(func):
        @wraps(func)
        def wrapper_timer(*args, **kwargs):
            if not hasattr(names, '__getitem__') and not all(isinstance(name, str) for name in names):
                raise TypeError('The names parameter expected to be a container of strings')
            out = {}
            if not all(hasattr(obj, name) for name in names):
                values = func(*args, **kwargs)
                for count, name in enumerate(names):
                    out[name] = values[count]
                    setattr(obj, name, values[count])
                return out, obj

            return
        return wrapper_timer
    return decorator


def call_tracker(func):
    @functools.wraps(func)
    def wrapper(*args):
        wrapper.has_been_called = True
        return func(*args)
    wrapper.has_been_called = False
    return wrapper


def counted(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        return f(*args, **kwargs)
    wrapped.calls = 0
    return wrapped


def cache_result(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        name = func.func_name
        out = None
        if not hasattr(self, name):
            out = func(self, *args, **kwargs)
            setattr(self, name, out)
        return out or getattr(self, name)
    return wrapper


class OptionalDecoratorDecorator:
    def __init__(self, decorator):
        self.deco = decorator

    def __call__(self, func):
        self.deco = self.deco(func)
        self.func = func

        def wrapped(*args, **kwargs):
            if kwargs.get("no_deco") is True:
                return self.func()
            else:
                return self.deco()
        return wrapped
