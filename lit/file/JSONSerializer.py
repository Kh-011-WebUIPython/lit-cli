import json

import lit.file.exception as exception
from lit.file.ISerializer import ISerializer


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

    def create_list_item(self, key):
        """Creates list item related to specified key"""

        '''Reading JSON data from file to temporary variable'''
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)

        '''If there exists such key, raise an exception'''
        if key in json_data.keys():
            raise exception.JSONKeyAlreadyExists(key)

        '''Create a list item assigned to specified key'''
        json_data[key] = list()

        '''Writing edited JSON data back to file (overwriting the old data)'''
        with open(self.file_worker.file_path, 'w') as file_object:
            json.dump(json_data, file_object)

    def append_to_list_item(self, key, new_item):
        """Appends value to list item in JSON file"""

        '''Reading JSON data from file to temporary variable'''
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)

        '''If there is no value assigned with the key, initialize the value with an empty list'''
        if key not in json_data.keys():
            json_data[key] = list()
        elif not isinstance(json_data[key], list):
            raise exception.JSONValueIsNotListError(key, json_data[key])

        '''Modifying JSON structure in temporary variable'''
        json_data[key].append(new_item)

        '''Writing edited JSON data back to file (overwriting the old data)'''
        with open(self.file_worker.file_path, 'w') as file_object:
            json.dump(json_data, file_object)

    def set_to_list_item(self, key, list_index, list_new_value):
        """Reading JSON data from file to temporary variable"""
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)

        '''Check if JSON data contains the key and if the key corresponds to list'''
        if key not in json_data.keys():
            raise exception.JSONDoesNotContainSuchKeyError(key)
        elif not isinstance(json_data[key], list):
            raise exception.JSONValueIsNotListError(key, json_data[key])

        '''Modifying JSON structure in temporary variable'''
        try:
            json_data[key][list_index] = list_new_value
        except IndexError:
            # TODO implement more convenient way of handling this error
            raise

        '''Writing edited JSON data back to file (overwriting the old data)'''
        with open(self.file_worker.file_path, 'w') as file_object:
            json.dump(json_data, file_object)

    def get_from_list_item(self, key, index):
        """Reading JSON data from file to temporary variable"""
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)

        '''If there is not value assigned with the key, initialize the value with an empty list'''
        if key not in json_data.keys():
            raise TypeError("Key '" + key + "' does not exist")
        elif not isinstance(json_data[key], list):
            raise TypeError("Key '" + key + "' does not correspond to list")

        try:
            return json_data[key][index]
        except IndexError:
            # TODO implement more convenient way of handling this error
            raise

    def get_all_from_list_item(self, key):
        """Reading JSON data from file to temporary variable"""
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)

        '''If there is not value assigned with the key, initialize the value with an empty list'''
        if key not in json_data.keys():
            raise TypeError("Key '" + key + "' does not exist")
        elif not isinstance(json_data[key], list):
            raise TypeError("Key '" + key + "' does not correspond to list")

        return json_data[key]

    def remove_from_list_item(self, key, index):
        """Reading JSON data from file to temporary variable"""
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)

        '''If there is not value assigned with the key, initialize the value with an empty list'''
        if key not in json_data.keys():
            raise exception.JSONDoesNotContainSuchKeyError(key)
        elif not isinstance(json_data[key], list):
            raise exception.JSONValueIsNotListError(key, json_data[key])

        '''Modifying JSON structure in temporary variable'''
        try:
            del json_data[key][index]
        except IndexError:
            # TODO implement more convenient way of handling this error
            raise

        '''Writing edited JSON data back to file (overwriting the old data)'''
        with open(self.file_worker.file_path, 'w') as file_object:
            json.dump(json_data, file_object)

    def remove_all_from_list_item(self, key):
        """Reading JSON data from file to temporary variable"""
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)

        '''If there is not value assigned with the key, initialize the value with an empty list'''
        if key not in json_data.keys():
            return False
        elif not isinstance(json_data[key], list):
            return False

        '''Modifying JSON structure in temporary variable'''
        del json_data[key][:]

        '''Writing edited JSON data back to file (overwriting the old data)'''
        with open(self.file_worker.file_path, 'w') as file_object:
            json.dump(json_data, file_object)
        return True

    def add_to_set_item(self, key, value):
        """Reading JSON data from file to temporary variable"""
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)

        '''If there is no value assigned with the key, initialize the value with an empty list'''
        if key not in json_data.keys():
            json_data[key] = list()
        elif not isinstance(json_data[key], list):
            raise exception.JSONValueIsNotListError(key, json_data[key])

        '''Converting to set'''
        json_data[key] = set(json_data[key])

        '''Modifying JSON structure in temporary variable'''
        json_data[key].add(value)

        '''Converting to list'''
        json_data[key] = list(json_data[key])

        '''Writing edited JSON data back to file (overwriting the old data)'''
        with open(self.file_worker.file_path, 'w') as file_object:
            json.dump(json_data, file_object)

    def add_set_to_set_item(self, key, set_value):
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)

        '''If there is no value assigned with the key, initialize the value with an empty list'''
        if key not in json_data.keys():
            json_data[key] = list()
        elif not isinstance(json_data[key], list):
            raise exception.JSONValueIsNotListError(key, json_data[key])

        '''Converting to set'''
        json_data[key] = set(json_data[key])

        for item in set_value:
            json_data[key].add(item)

        '''Converting to list'''
        json_data[key] = list(json_data[key])

        '''Writing edited JSON data back to file (overwriting the old data)'''
        with open(self.file_worker.file_path, 'w') as file_object:
            json.dump(json_data, file_object)

    def get_all_from_set_item(self, key):
        """Reading JSON data from file to temporary variable"""
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)

        '''If there is not value assigned with the key, initialize the value with an empty list'''
        if key not in json_data.keys():
            raise TypeError("Key '" + key + "' does not exist")
        elif not isinstance(json_data[key], list):
            raise TypeError("Key '" + key + "' does not correspond to set")

        return set(json_data[key])

    def remove_from_set_item(self, key, value):
        result = True
        """Reading JSON data from file to temporary variable"""
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)

        '''If there is no value assigned with the key, initialize the value with an empty list'''
        if key not in json_data.keys():
            raise exception.JSONDoesNotContainSuchKeyError(key)
        elif not isinstance(json_data[key], list):
            raise exception.JSONValueIsNotListError(key, json_data[key])

        '''Converting to set'''
        json_data[key] = set(json_data[key])

        '''Modifying JSON structure in temporary variable'''
        try:
            json_data[key].remove(value)
        except KeyError:
            result = False

        '''Converting to list'''
        json_data[key] = list(json_data[key])

        '''Writing edited JSON data back to file (overwriting the old data)'''
        with open(self.file_worker.file_path, 'w') as file_object:
            json.dump(json_data, file_object)

        return result

    def remove_set_from_set_item(self, key, set_value):
        result = True
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)

        '''If there is no value assigned with the key, initialize the value with an empty list'''
        if key not in json_data.keys():
            raise exception.JSONDoesNotContainSuchKeyError(key)
        elif not isinstance(json_data[key], list):
            raise exception.JSONValueIsNotListError(key, json_data[key])

        '''Converting to set'''
        json_data[key] = set(json_data[key])

        '''Modifying JSON structure in temporary variable'''
        try:
            for item in set_value:
                json_data[key].remove(item)
        except KeyError:
            result = False

        '''Converting to list'''
        json_data[key] = list(json_data[key])

        '''Writing edited JSON data back to file (overwriting the old data)'''
        with open(self.file_worker.file_path, 'w') as file_object:
            json.dump(json_data, file_object)

        return result

    def set_value(self, key, value):
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)
        json_data[key] = value
        with open(self.file_worker.file_path, 'w') as file_object:
            json.dump(json_data, file_object)

    def set_values(self, values):
        with open(self.file_worker.file_path, 'r') as file_object:
            json_data = json.load(file_object)
        for k, v in values.items():
            json_data[k] = v
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
