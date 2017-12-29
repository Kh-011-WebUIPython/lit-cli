import os

from tests import util
import unittest

''' Need to run here to change working directory before strings_holder import '''
os.chdir(util.TEST_DIR_PATH)

from lit.strings_holder import AddStrings, TrackedFileSettings
from lit.command.AddCommand import AddCommand
from lit.command.InitCommand import InitCommand
from lit.file.JSONSerializer import JSONSerializer
import lit.util


class TestAddCommand(unittest.TestCase):
    def setUp(self):
        InitCommand().run()
        with open(util.TEST_FILE_1_PATH, 'w') as file:
            file.write(util.TEST_FILE_1_CONTENT)

    def tearDown(self):
        lit.util.clear_dir_content(util.TEST_DIR_PATH)

    def test_file_addition(self):
        self.assertTrue(AddCommand().run(**{
            AddStrings.ARG_PATH_NAME: util.TEST_FILE_1_NAME,
        }))
        tracked_file_path = TrackedFileSettings.FILE_PATH
        file_list = JSONSerializer(tracked_file_path).get_all_from_list_item(
            TrackedFileSettings.FILES_KEY)
        with open(TrackedFileSettings.FILE_PATH) as file:
            self.assertEqual(1, len(file_list),
                             ("'" + TrackedFileSettings.FILE_PATH + "' content:" + os.linesep + file.read()))
            self.assertEqual(file_list[0], util.TEST_FILE_1_NAME)

    def test_file_addition_that_does_not_exist(self):
        self.assertFalse(AddCommand().run(**{
            AddStrings.ARG_PATH_NAME: util.TEST_NONEXISTENT_FILE_NAME,
        }))
