class DescriptorNamingMeta(type):

    def __new__(mcs, name, bases, namespace):
        for name, attr in namespace.items():
            if isinstance(attr, Named):
                attr.name = name
        return super().__new__(mcs, name, bases, namespace)

    def __getitem__(self, item, key):
        if isinstance(item, dict):
            return item[key]
        else:
            return item


class Named:

    def __init__(self, name=None):
        self.name = name
