from lit.file.ISerializer import ISerializer
from lit.file.JSONSerializer import JSONSerializer
import lit.file.exception as exception


class StringManager():

    def __init__(self):
        raise TypeError('StringManager is not designed to create its instances')

    @classmethod
    def init(cls, serializer):
        if not issubclass(type(serializer), ISerializer):
            raise TypeError('ISerializer implementations supported only, not ' + str(type(serializer)))
        cls.__serializer = serializer

    @classmethod
    def get_string(cls, key):
        try:
            value = cls.__serializer.get_value(key)
            if value is None:
                value = key
        except AttributeError as err:
            raise exception.SerializerIsNotSetError() from err
        return value

    @classmethod
    def set_string(cls, key, value):
        try:
            cls.__serializer.set_value(key, value)
        except AttributeError as err:
            raise exception.SerializerIsNotSetError() from err
