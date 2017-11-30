import abc
from lit.file.FileWorker import FileWorker


class ISerializer(abc.ABC):
    def __init__(self, file_path):
        self.__file_worker = FileWorker(file_path)

    @abc.abstractmethod
    def append_to_list_item(self, key, new_item):
        pass

    @abc.abstractmethod
    def read_all_items(self):
        pass

    @abc.abstractmethod
    def get_items_count(self):
        pass

    @property
    def file_worker(self):
        return self.__file_worker
