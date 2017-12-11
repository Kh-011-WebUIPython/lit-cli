from lit.file.ISerializer import ISerializer


class SettingsManager():
    def __init__(self):
        raise TypeError('SettingsManager is not designed to create its instances')

    @classmethod
    def init(cls, serializer):
        if not issubclass(type(serializer), ISerializer):
            raise TypeError('ISerializer implementations supported only')
        cls.__serializer = serializer

    @classmethod
    def get_var_value(cls, var_key):
        value = cls.__serializer.get_value(var_key)
        if value is None:
            raise RuntimeError('Setting variable \'' + var_key + '\' not found')
        return value

    @classmethod
    def set_var_value(cls, var_key, var_new_value):
        cls.__serializer.set_value(var_key, var_new_value)
