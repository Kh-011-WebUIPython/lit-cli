from lit.file.ISerializer import ISerializer


class CommitsHistoryManager():
    def __init__(self, serializer):
        if serializer is not ISerializer:
            raise TypeError('ISerializer implementations supported only')
        self.__serializer = serializer

    def write_commit_log(self, message, datetime):
        raise NotImplementedError()

    def read_all_commits(self):
        raise NotImplementedError()

    def get_commits_count(self):
        raise NotImplementedError()
