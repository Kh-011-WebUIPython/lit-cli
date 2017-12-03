from datetime import datetime
from lit.file.ISerializer import ISerializer
import lit.file.exception as exception


class CommitsHistoryManager():
    LIST_KEY = 'commits'
    DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S-%f'

    COMMIT_DATETIME_KEY = 'datetime'
    COMMIT_MESSAGE_KEY = 'message'

    @classmethod
    def init(cls, serializer):
        if not issubclass(type(serializer), ISerializer):
            raise TypeError('ISerializer implementations supported only')
        cls.__serializer = serializer

    @classmethod
    def write_commit_info(cls, message, date_time=datetime.now()):
        date_time_str = date_time.strftime(cls.DATETIME_FORMAT)
        commit_info = {cls.COMMIT_DATETIME_KEY: date_time_str, cls.COMMIT_MESSAGE_KEY: message}
        try:
            cls.__serializer.append_to_list_item(cls.LIST_KEY, commit_info)
        except AttributeError as err:
            raise exception.SerializerIsNotSetError() from err

    @classmethod
    def read_all_commits(cls):
        try:
            commits = cls.__serializer.get_all_from_list_item(cls.LIST_KEY)
        except AttributeError as err:
            raise exception.SerializerIsNotSetError() from err
        return commits

    @classmethod
    def get_commits_count(cls):
        try:
            return len(cls.read_all_commits())
        except AttributeError as err:
            raise exception.SerializerIsNotSetError() from err

    @classmethod
    def __clear_commits_info(cls):
        try:
            cls.__serializer.remove_all_from_list_item(cls.LIST_KEY)
        except AttributeError as err:
            raise exception.SerializerIsNotSetError() from err
