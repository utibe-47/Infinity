from weakref import WeakKeyDictionary

from utilities.datetime_helpers import DateHelpers
from .meta_helpers import Named


class RunDateChecker(Named):

    def __init__(self, name=None):
        super().__init__(name)
        self._instance_data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._instance_data[instance]

    def __set__(self, instance, value):
        if value is None:
            self._instance_data[instance] = value
        else:
            try:
                val = DateHelpers.convert_dt_to_str(value)
            except TypeError as err:
                raise TypeError("A date in the wrong format was specified for the run "
                                "date. See error: {}".format(str(err)))
            else:
                self._instance_data[instance] = val

    def __delete__(self, instance):
        raise AttributeError("Cannot delete attribute {}".format(self.name))
