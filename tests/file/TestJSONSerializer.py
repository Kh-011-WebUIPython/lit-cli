import unittest
import os
import json
from lit.file.JSONSerializer import JSONSerializer

TEST_JSON_FILE_PATH = 'test_json.json'


class TestJSONSerializer(unittest.TestCase):
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

    def _remove_test_file_if_exists(self):
        try:
            os.remove(TEST_JSON_FILE_PATH)
        except FileNotFoundError:
            pass

    def setUp(self):
        self._remove_test_file_if_exists()

    def tearDown(self):
        self._remove_test_file_if_exists()

    def test_append_item_to_new_file_success(self):
        serializer = JSONSerializer(TEST_JSON_FILE_PATH)

        serializer.append_item(self.item1)
        with open(TEST_JSON_FILE_PATH, 'r') as file_object:
            json_data = json.load(file_object)
            expected_string = '[' + str(self.item1) + ']'
            actual_string = str(json_data)
            self.assertTrue(actual_string == expected_string, '\n' + actual_string + '\n' + expected_string)
        os.remove(TEST_JSON_FILE_PATH)

    def test_append_item_to_existing_file_success(self):
        serializer = JSONSerializer(TEST_JSON_FILE_PATH)
        serializer.append_item(self.item1)

        serializer = JSONSerializer(TEST_JSON_FILE_PATH)
        serializer.append_item(self.item2)
        with open(TEST_JSON_FILE_PATH, 'r') as file_object:
            json_data = json.load(file_object)
            expected_string = str(self.item2)
            actual_string = str(json_data[len(json_data) - 1])
            self.assertFalse(len(json_data) == 1, len(json_data))
            self.assertTrue(actual_string == expected_string, '\n' + actual_string + '\n' + expected_string)

    def test_read_all_items_success(self):
        serializer = JSONSerializer(TEST_JSON_FILE_PATH)

        serializer.append_item(self.item1)
        serializer.append_item(self.item2)
        with open(TEST_JSON_FILE_PATH, 'r') as file_object:
            json_data = json.load(file_object)
            expected_string = '[' + str(self.item1) + ', ' + str(self.item2) + ']'
            actual_string = str(json_data)
            self.assertTrue(actual_string == expected_string, '\n' + actual_string + '\n' + expected_string)

    def test_get_items_count(self):
        serializer = JSONSerializer(TEST_JSON_FILE_PATH)

        serializer.append_item(self.item1)
        with open(TEST_JSON_FILE_PATH, 'r') as file_object:
            json_data = json.load(file_object)
            expected_value = 1
            actual_value = len(json_data)
            self.assertEqual(expected_value, actual_value)

        serializer.append_item(self.item2)
        with open(TEST_JSON_FILE_PATH, 'r') as file_object:
            json_data = json.load(file_object)
            expected_value = 2
            actual_value = len(json_data)
            self.assertEqual(expected_value, actual_value)

if __name__ == '__main__':
    unittest.main()
