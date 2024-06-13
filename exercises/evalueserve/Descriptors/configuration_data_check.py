from weakref import WeakKeyDictionary

from .enums import RequiredInputs
from .meta_helpers import Named


class ConfigDataCheck(Named):

    """
    Descriptor for input config data to ensure that it is always contains the required attributes
    """

    def __init__(self, name=None):
        super().__init__(name)
        self._instance_data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._instance_data[instance]

    def __set__(self, instance, value):
        if isinstance(value, dict) and len(value) > 0:
            if any(key not in value.keys() for key in RequiredInputs.__members__.keys()):
                raise AttributeError('The configuration file needs to contain all the attributes defined in the '
                                     'required inputs file')
            self._instance_data[instance] = value
        else:
            raise TypeError('Attribute value {} must be a dictionary. Input of type {} was specified'.
                            format(self.name, type(value)))

    def __delete__(self, instance):
        raise AttributeError("Cannot delete attribute {}".format(self.name))
