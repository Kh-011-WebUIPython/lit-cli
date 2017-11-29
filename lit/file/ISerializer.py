import abc
from lit.file.FileWorker import FileWorker


class ISerializer(abc.ABC):
    def __init__(self, file_path):
        self.__file_worker = FileWorker(file_path)

    @abc.abstractmethod
    def write_item(self):
        pass

    @abc.abstractmethod
    def read_all_items(self):
        pass

    @abc.abstractmethod
    def get_items_count(self):
        pass
