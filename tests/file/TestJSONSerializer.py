import unittest
import os
import json
from lit.file.JSONSerializer import JSONSerializer

TEST_JSON_FILE_PATH = 'test_json.json'


class TestJSONSerializer(unittest.TestCase):
    list_key = 'items'
    item1 = {'key1': 'value1',
             'key2': 'value2',
             'key3': 'value3',
             'key4': 'value4',
             'key5': 'value5',
             }
    item2 = {'key11': 'value11',
             'key12': 'value12',
             'key13': 'value13',
             'key14': 'value14',
             'key15': 'value15',
             }

    @staticmethod
    def __remove_test_file_if_exists():
        try:
            os.remove(TEST_JSON_FILE_PATH)
        except FileNotFoundError:
            pass

    def setUp(self):
        self.__remove_test_file_if_exists()

    def tearDown(self):
        self.__remove_test_file_if_exists()

    def test_append_item_to_new_file_success(self):
        serializer = JSONSerializer(TEST_JSON_FILE_PATH)

        serializer.append_to_list_item(self.list_key, self.item1)
        with open(TEST_JSON_FILE_PATH, 'r') as file_object:
            json_data = json.load(file_object)
            expected_string = '[' + str(self.item1) + ']'
            actual_string = str(json_data[self.list_key])
            self.assertTrue(actual_string == expected_string, '\n' + actual_string + '\n' + expected_string)
        os.remove(TEST_JSON_FILE_PATH)

    def test_append_item_to_existing_file_success(self):
        serializer = JSONSerializer(TEST_JSON_FILE_PATH)
        serializer.append_to_list_item(self.list_key, self.item1)

        serializer = JSONSerializer(TEST_JSON_FILE_PATH)
        serializer.append_to_list_item(self.list_key, self.item2)
        with open(TEST_JSON_FILE_PATH, 'r') as file_object:
            json_data = json.load(file_object)
            expected_string = str(self.item2)
            actual_string = str(json_data[self.list_key][len(json_data[self.list_key]) - 1])
            self.assertFalse(len(json_data[self.list_key]) == 1, len(json_data[self.list_key]))
            self.assertTrue(actual_string == expected_string, '\n' + actual_string + '\n' + expected_string)

    def test_read_all_items_success(self):
        serializer = JSONSerializer(TEST_JSON_FILE_PATH)

        serializer.append_to_list_item(self.list_key, self.item1)
        serializer.append_to_list_item(self.list_key, self.item2)
        with open(TEST_JSON_FILE_PATH, 'r') as file_object:
            json_data = json.load(file_object)
            expected_string = '[' + str(self.item1) + ', ' + str(self.item2) + ']'
            actual_string = str(json_data[self.list_key])
            self.assertTrue(actual_string == expected_string, '\n' + actual_string + '\n' + expected_string)

    def test_get_items_count(self):
        serializer = JSONSerializer(TEST_JSON_FILE_PATH)

        serializer.append_to_list_item(self.list_key, self.item1)
        with open(TEST_JSON_FILE_PATH, 'r') as file_object:
            json_data = json.load(file_object)
            expected_value = 1
            actual_value = len(json_data)
            self.assertEqual(expected_value, actual_value)

        serializer.append_to_list_item(self.list_key, self.item2)
        with open(TEST_JSON_FILE_PATH, 'r') as file_object:
            json_data = json.load(file_object)
            expected_value = 2
            actual_value = len(json_data[self.list_key])
            self.assertEqual(expected_value, actual_value)

    def test_set_values(self):
        serializer = JSONSerializer(TEST_JSON_FILE_PATH)

        serializer.set_values(self.item1)
        with open(TEST_JSON_FILE_PATH, 'r') as file_object:
            json_data = json.load(file_object)
            for key in self.item1.keys():
                self.assertIn(key, json_data.keys())
                self.assertEqual(self.item1[key], json_data[key])
            self.assertEqual(len(self.item1), len(json_data))


if __name__ == '__main__':
    unittest.main()
