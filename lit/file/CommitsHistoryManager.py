from datetime import datetime
from lit.file.ISerializer import ISerializer
import lit.file.exception as exception


class CommitsHistoryManager():
    LIST_KEY = 'commits'
    DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S-%f'

    COMMIT_DATETIME_KEY = 'datetime'
    COMMIT_MESSAGE_KEY = 'message'
    COMMIT_HASH_KEY = 'hash'
    COMMIT_USER_NAME_KEY = 'username'
    COMMIT_USER_EMAIL_KEY = 'email'

    @classmethod
    def init(cls, serializer):
        if not issubclass(type(serializer), ISerializer):
            raise TypeError('ISerializer implementations supported only')
        cls.__serializer = serializer

    @classmethod
    def write_commit_info(
            cls, commit_message, commit_hash, commit_user_name,
            commit_user_email, commit_datetime=datetime.now()):
        date_time_str = commit_datetime.strftime(cls.DATETIME_FORMAT)
        commit_info = {
            cls.COMMIT_DATETIME_KEY: date_time_str,
            cls.COMMIT_HASH_KEY: commit_hash,
            cls.COMMIT_USER_EMAIL_KEY: commit_user_email,
            cls.COMMIT_USER_NAME_KEY: commit_user_name,
            cls.COMMIT_MESSAGE_KEY: commit_message,
        }
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
