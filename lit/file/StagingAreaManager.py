from lit.file.ISerializer import ISerializer
import lit.file.exception as exception


class StagingAreaManager():
    SET_KEY = 'files'

    @classmethod
    def init(cls, serializer):
        if not issubclass(type(serializer), ISerializer):
            raise TypeError('ISerializer implementations supported only')
        cls.__serializer = serializer

    @classmethod
    def add_file(cls, file_name):
        try:
            cls.__serializer.add_to_set_item(cls.SET_KEY, file_name)
        except AttributeError as err:
            raise exception.SerializerIsNotSetError() from err

    @classmethod
    def remove_file(cls, file_name):
        try:
            cls.__serializer.remove_from_set_item(cls.SET_KEY, file_name)
        except AttributeError as err:
            raise exception.SerializerIsNotSetError() from err
        except KeyError:
            return False
        return True

    @classmethod
    def get_tracked_files(cls):
        try:
            files = cls.__serializer.get_all_from_set_item(cls.SET_KEY)
        except AttributeError as err:
            raise exception.SerializerIsNotSetError() from err
        return files

    @classmethod
    def get_tracked_files_count(cls):
        return len(cls.get_tracked_files())
