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


class JSONValueIsNotSetError(JSONError):
    def __init__(self, key, value):
        self.__key = key
        self.__value = value

    def __str__(self):
        return 'The value ' + self.__value + ' must be set, not ' + type(self.__value)


class JSONDoesNotContainSuchKeyError(JSONError):
    def __init__(self, key):
        self.__key = key

    def __str__(self):
        return 'The key ' + self.__key + ' was not found'


class JSONKeyAlreadyExists(JSONError):
    def __init__(self, key):
        self.__key = key

    def __str__(self):
        return 'The key ' + self.__key + ' already exists'


class SerializerIsNotSetError(Exception):
    def __init__(self):
        pass
