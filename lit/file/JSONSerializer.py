import json
from lit.file.ISerializer import ISerializer


class JSONSerializer(ISerializer):
    def __init__(self, file_path):
        super().__init__(file_path)
        try:
            with open(self.file_worker.file_path, 'r') as file_object:
                json.load(file_object)
        except json.decoder.JSONDecodeError:
            self.__init_empty_list_in_json_file()

    def __init_empty_list_in_json_file(self):
        with open(self.file_worker.file_path, 'w') as file_object:
            json.dump(list(), file_object)

    def append_item(self, item):
        """Appends an object to existing JSON file"""

        '''Reading JSON data from file to temporary variable'''
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)
        '''Modifying JSON structure in temporary variable'''
        json_data.append(item)
        '''Writing edited JSON data back to file (overwriting the old data)'''
        with open(self.file_worker.file_path, 'w') as file_object:
            json.dump(json_data, file_object)

    def read_all_items(self):
        """Reads all items in file"""
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)
            return json_data

    def get_items_count(self):
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)
            return len(json_data)
