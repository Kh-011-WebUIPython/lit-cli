from datetime import datetime
from lit.file.ISerializer import ISerializer


class CommitsHistoryManager():
    FILE_PATH = 'commits.json'
    DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S-%f'

    def __init__(self, serializer):
        if serializer is not ISerializer:
            raise TypeError('ISerializer implementations supported only')
        self.__serializer = serializer

    def write_commit_info(self, message, datetime=datetime.now()):
        commit_info = {'message': message, 'datetime': datetime}
        self.serializer.append_item(commit_info)
        raise NotImplementedError()

    def read_all_commits(self):
        raise NotImplementedError()

    def get_commits_count(self):
        raise NotImplementedError()

    @property
    def serializer(self):
        return self.__serializer

    def __clear_commits_info(self):
        raise NotImplementedError()
