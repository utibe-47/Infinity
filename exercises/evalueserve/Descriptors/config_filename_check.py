from weakref import WeakKeyDictionary

from .meta_helpers import Named


class ConfigurationFileNameCheck(Named):

    def __init__(self, name=None):
        super().__init__(name)
        self._instance_data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._instance_data[instance]

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError('{} must be a string. Input of type {} was specified'.format(self.name, type(value)))
        file_type = '.json'
        if bool(value) and file_type in value:
            self._instance_data[instance] = value
        else:
            raise AttributeError('Attribute {} must be a non empty, the file name for a json file'.format(self.name))

    def __delete__(self, instance):
        raise AttributeError("Cannot delete attribute {}".format(self.name))
