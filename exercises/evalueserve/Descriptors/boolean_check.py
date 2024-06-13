from weakref import WeakKeyDictionary
from .meta_helpers import Named


def str_to_bool(s):
    if s == 'True' or s == 'Y':
         return True
    elif s == 'False' or s == 'F':
         return False
    else:
         raise ValueError


class BooleanCheck(Named):

    def __init__(self, name=None):
        super().__init__(name)
        self._instance_data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._instance_data[instance]

    def __set__(self, instance, value):
        if not isinstance(value, bool):
            if isinstance(value, str):
                try:
                    self._instance_data[instance] = str_to_bool(value)
                except ValueError:
                    raise TypeError('Attribute value {} must be a boolean. Input of type {} was '
                                    'specified'.format(self.name, type(value)))
            else:
                raise TypeError('Attribute value {} must be a boolean. Input of type {} was '
                                'specified'.format(self.name, type(value)))
        else:
            self._instance_data[instance] = value

    def __delete__(self, instance):
        raise AttributeError("Cannot delete attribute {}".format(self.name))
