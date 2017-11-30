class FileError(Exception):
    pass


class JSONError(FileError):
    pass


class JSONValueIsNotListError(JSONError):
    def __init__(self, key, value):
        self.__key = key
        self.__value = value

    def __str__(self):
        return 'The value ' + self.__value + ' must be list, not ' + type(self.__value)
