from weakref import WeakKeyDictionary
from .meta_helpers import Named


class IsNonEmptyDictionary(Named):

    """
    Descriptor for input data to ensure that it is always a  non empty dictionary
    """

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
            if isinstance(value, dict) and len(value) > 0:
                self._instance_data[instance] = value
            else:
                raise TypeError('Attribute value {} must be a non empty dictionary. Input of type {} was specified'.
                                format(self.name, type(value)))

    def __delete__(self, instance):
        raise AttributeError("Cannot delete attribute {}".format(self.name))
