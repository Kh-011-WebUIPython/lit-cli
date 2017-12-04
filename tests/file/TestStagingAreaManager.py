import unittest
import os
from lit.file.JSONSerializer import JSONSerializer
from lit.file.StagingAreaManager import StagingAreaManager

TEST_JSON_FILE_PATH = 'test_json.json'


class TestStagingAreaManager(unittest.TestCase):
    FILE_NAME_1 = 'file1.py'
    FILE_NAME_2 = 'file2.py'

    @staticmethod
    def __remove_test_file_if_exists():
        try:
            os.remove(TEST_JSON_FILE_PATH)
        except FileNotFoundError:
            pass

    def setUp(self):
        self.__remove_test_file_if_exists()
        self.serializer = JSONSerializer(TEST_JSON_FILE_PATH)
        StagingAreaManager.init(self.serializer)

    def tearDown(self):
        self.__remove_test_file_if_exists()

    def test_add_file(self):
        StagingAreaManager.add_file(self.FILE_NAME_1)

        files = self.serializer.get_all_from_set_item(StagingAreaManager.SET_KEY)
        self.assertIn(self.FILE_NAME_1, files)
        self.assertNotIn(self.FILE_NAME_2, files)

    def test_remove_file(self):
        StagingAreaManager.add_file(self.FILE_NAME_1)
        StagingAreaManager.add_file(self.FILE_NAME_2)

        files = self.serializer.get_all_from_set_item(StagingAreaManager.SET_KEY)
        self.assertIn(self.FILE_NAME_1, files)
        self.assertIn(self.FILE_NAME_2, files)
        self.assertEqual(2, len(files))
        StagingAreaManager.remove_file(self.FILE_NAME_1)
        files = self.serializer.get_all_from_set_item(StagingAreaManager.SET_KEY)
        self.assertNotIn(self.FILE_NAME_1, files)
        self.assertIn(self.FILE_NAME_2, files)
        self.assertEqual(1, len(files))

    def test_get_tracked_files(self):
        StagingAreaManager.add_file(self.FILE_NAME_1)
        files = self.serializer.get_all_from_set_item(StagingAreaManager.SET_KEY)
        self.assertIn(self.FILE_NAME_1, files)
        self.assertNotIn(self.FILE_NAME_2, files)
        self.assertEqual(1, len(files))
        StagingAreaManager.add_file(self.FILE_NAME_2)
        files = self.serializer.get_all_from_set_item(StagingAreaManager.SET_KEY)
        self.assertIn(self.FILE_NAME_1, files)
        self.assertIn(self.FILE_NAME_2, files)
        self.assertEqual(2, len(files))

    def test_get_tracked_files_count(self):
        StagingAreaManager.add_file(self.FILE_NAME_1)
        files = self.serializer.get_all_from_set_item(StagingAreaManager.SET_KEY)
        self.assertEqual(1, len(files))
        StagingAreaManager.add_file(self.FILE_NAME_1)
        files = self.serializer.get_all_from_set_item(StagingAreaManager.SET_KEY)
        self.assertEqual(1, len(files))
        StagingAreaManager.add_file(self.FILE_NAME_2)
        files = self.serializer.get_all_from_set_item(StagingAreaManager.SET_KEY)
        self.assertEqual(2, len(files))
        StagingAreaManager.remove_file(self.FILE_NAME_1)
        files = self.serializer.get_all_from_set_item(StagingAreaManager.SET_KEY)
        self.assertEqual(1, len(files))
        StagingAreaManager.remove_file(self.FILE_NAME_1)
        files = self.serializer.get_all_from_set_item(StagingAreaManager.SET_KEY)
        self.assertEqual(1, len(files))
        StagingAreaManager.remove_file(self.FILE_NAME_2)
        files = self.serializer.get_all_from_set_item(StagingAreaManager.SET_KEY)
        self.assertEqual(0, len(files))
