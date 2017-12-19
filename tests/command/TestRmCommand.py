import os

from tests import util
import unittest

''' Need to run here to change working directory before strings_holder import '''
os.chdir(util.TEST_DIR_PATH)

from lit.strings_holder import AddStrings, RmStrings, TrackedFileSettings
from lit.command.AddCommand import AddCommand
from lit.command.RmCommand import RmCommand
from lit.command.InitCommand import InitCommand
from lit.file.JSONSerializer import JSONSerializer
import lit.util


class TestRmCommand(unittest.TestCase):
    def setUp(self):
        InitCommand().run()
        with open(util.TEST_FILE_1_PATH, 'w') as file:
            file.write(util.TEST_FILE_1_CONTENT)
        with open(util.TEST_FILE_2_PATH, 'w') as file:
            file.write(util.TEST_FILE_2_CONTENT)
        AddCommand().run(**{
            AddStrings.ARG_PATH_NAME: '.',
        })

    def tearDown(self):
        lit.util.clear_dir_content(util.TEST_DIR_PATH)

    def test_files_from_staging_area_removal(self):
        self.assertTrue(RmCommand().run(**{
            RmStrings.ARG_PATH_NAME: util.TEST_FILE_1_NAME,
        }))
        tracked_file_path = os.path.join(util.TEST_DIR_PATH, TrackedFileSettings.FILE_PATH)
        file_list = JSONSerializer(tracked_file_path).get_all_from_list_item(
            TrackedFileSettings.FILES_KEY)
        self.assertEqual(1, len(file_list))
        self.assertEqual(file_list[0], util.TEST_FILE_2_NAME)

    def test_remove_file_entry_from_list_which_is_absent(self):
        self.assertFalse(RmCommand().run(**{
            RmStrings.ARG_PATH_NAME: util.TEST_NONEXISTENT_FILE_NAME,
        }))
        tracked_file_path = os.path.join(util.TEST_DIR_PATH, TrackedFileSettings.FILE_PATH)
        file_list = JSONSerializer(tracked_file_path).get_all_from_list_item(
            TrackedFileSettings.FILES_KEY)
        self.assertEqual(2, len(file_list))
        self.assertIn(util.TEST_FILE_1_NAME, file_list)
        self.assertIn(util.TEST_FILE_2_NAME, file_list)
