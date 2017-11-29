from lit.file.ISerializer import ISerializer


class StagingAreaManager():
    def __init__(self, serializer):
        if serializer is not ISerializer:
            raise TypeError('ISerializer implementations supported only')
        self.__serializer = serializer

    def add_file(self, file_name):
        raise NotImplementedError()

    def remove_file(self, file_name):
        raise NotImplementedError()

    def get_tracked_files(self):
        raise NotImplementedError()
