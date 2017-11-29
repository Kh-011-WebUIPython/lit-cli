import json
from lit.file.ISerializer import ISerializer


class JSONSerializer(ISerializer):
    def __init__(self, file_path):
        super().__init__(file_path)

    def write_item(self):
        raise NotImplementedError()

    def read_all_items(self):
        raise NotImplementedError()

    def get_items_count(self):
        raise NotImplementedError()
