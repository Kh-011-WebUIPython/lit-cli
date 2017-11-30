from lit.file.ISerializer import ISerializer


class SettingsManager():
    def __init__(self, serializer):
        if serializer is not ISerializer:
            raise TypeError('ISerializer implementations supported only')
        self.__serializer = serializer

    def get_var_value(self):
        pass

    def set_var_value(self):
        pass