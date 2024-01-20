from weakref import WeakKeyDictionary
from .meta_helpers import Named


class StringCheck(Named):

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
            if not isinstance(value, str):
                if isinstance(value, list):
                    self._instance_data[instance] = value
                else:
                    raise TypeError('Attribute value {} must be a string. Input of type {} was '
                                    'specified'.format(self.name, type(value)))
            else:
                self._instance_data[instance] = value

    def __delete__(self, instance):
        raise AttributeError("Cannot delete attribute {}".format(self.name))
