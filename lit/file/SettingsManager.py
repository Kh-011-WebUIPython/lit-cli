from lit.file.ISerializer import ISerializer


class SettingsManager():
    def __init__(self, serializer):
        if not issubclass(type(serializer), ISerializer):
            raise TypeError('ISerializer implementations supported only')
        self.__serializer = serializer

    def get_var_value(self, var_key):
        return self.serializer.get_value(var_key)

    def set_var_value(self, var_key, var_new_value):
        self.serializer.set_value(var_key, var_new_value)

    @property
    def serializer(self):
        return self.__serializer
