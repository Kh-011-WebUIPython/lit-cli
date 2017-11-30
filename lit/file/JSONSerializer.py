import json
from lit.file.ISerializer import ISerializer
import lit.file.exception as exception


class JSONSerializer(ISerializer):
    def __init__(self, file_path):
        super().__init__(file_path)
        try:
            with open(self.file_worker.file_path, 'r') as file_object:
                json.load(file_object)
        except json.decoder.JSONDecodeError:
            self.__init_empty_dict_in_json_file()

    def __init_empty_dict_in_json_file(self):
        with open(self.file_worker.file_path, 'w') as file_object:
            json.dump(dict(), file_object)

    def append_to_list_item(self, key, new_item):
        """Appends value to list item in JSON file"""

        '''Reading JSON data from file to temporary variable'''
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)

        '''If there is not value assigned with the key, initialize the value with an empty list'''
        if key not in json_data.keys():
            json_data[key] = list()
        elif not isinstance(json_data[key], list):
            raise exception.JSONValueIsNotListError(key, json_data[key])
        '''Modifying JSON structure in temporary variable'''
        json_data[key].append(new_item)

        '''Writing edited JSON data back to file (overwriting the old data)'''
        with open(self.file_worker.file_path, 'w') as file_object:
            json.dump(json_data, file_object)

    def set_to_list_item(self, key, new_value):
        raise NotImplementedError()

    def remove_from_list_item(self, key, index):
        '''Reading JSON data from file to temporary variable'''
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)

        '''If there is not value assigned with the key, initialize the value with an empty list'''
        if key not in json_data.keys():
            return False
        elif not isinstance(json_data[key], list):
            return False
        '''Modifying JSON structure in temporary variable'''
        try:
            del json_data[key][index]
        except IndexError:
            # TODO implement more convenient way of handling this error
            return False
        '''Writing edited JSON data back to file (overwriting the old data)'''
        with open(self.file_worker.file_path, 'w') as file_object:
            json.dump(json_data, file_object)

    def set_value(self, key, value):
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)
        json_data[key] = value
        with open(self.file_worker.file_path, 'w') as file_object:
            json.dump(json_data, file_object)

    def get_value(self, key):
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)
        if key in json_data.keys():
            return json_data[key]
        return None

    def read_all_items(self):
        """Reads all items in file"""
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)
            return json_data

    def get_items_count(self):
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)
            return len(json_data)
