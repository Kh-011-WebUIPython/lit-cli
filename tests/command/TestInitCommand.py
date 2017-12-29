import sys
import os
import io
import unittest

from tests import util

''' Need to run here to change working directory before strings_holder import '''
os.chdir(util.TEST_DIR_PATH)

from lit.command.InitCommand import InitCommand
from lit.strings_holder import ProgramSettings, InitStrings, TrackedFileSettings, LogSettings, CommitSettings
import lit.util


class TestInitCommand(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ProgramSettings.LIT_PATH = os.path.join(util.TEST_DIR_PATH, ProgramSettings.LIT_DIR)

    def setUp(self):
        if not os.path.isdir(util.TEST_DIR_PATH):
            raise EnvironmentError('Could not find test dir \'' + util.TEST_DIR_PATH + '\'')
        if len(os.listdir(util.TEST_DIR_PATH)) != 0:
            lit.util.clear_dir_content(util.TEST_DIR_PATH)

    def tearDown(self):
        lit.util.clear_dir_content(util.TEST_DIR_PATH)

    def test_check_dot_lit_dir_content(self):
        self.assertTrue(InitCommand().run())
        lit_path = ProgramSettings.LIT_PATH
        self.assertTrue(os.path.isdir(lit_path), lit_path)
        expected_files = {ProgramSettings.LIT_SETTINGS_NAME,
                          TrackedFileSettings.FILE_NAME,
                          lit.util.get_current_branch_log_file_name()}
        expected_dirs = {CommitSettings.DIR_NAME}
        dir_items = os.listdir(lit_path)
        self.assertEqual(4, len(dir_items), 'dir items: ' + str(dir_items))
        print(str(dir_items))
        for item in dir_items:
            item_path = os.path.join(lit_path, item)
            if os.path.isfile(item_path):
                self.assertIn(item, expected_files)
                expected_files.remove(item)
            elif os.path.isdir(item_path):
                self.assertIn(item, expected_dirs)
                self.assertEqual(0, len(os.listdir(item_path)))
                expected_dirs.remove(item)
            else:
                raise AssertionError
        self.assertEqual(0, len(expected_files))
        self.assertEqual(0, len(expected_dirs))

    def test_check_repeated_repo_init(self):
        """ Check processing of init command for already inited repo """

        ''' redirecting standard output stream '''
        stdout = sys.stdout
        custom_stdout = io.StringIO()
        sys.stdout = custom_stdout

        ''' creating and running init command '''
        command = InitCommand()
        self.assertTrue(command.run())

        ''' saving repo settings files' last modification timestamps '''
        dir_items_with_mod_time = {}
        for item in os.listdir(util.TEST_DIR_PATH):
            item_path = os.path.join(util.TEST_DIR_PATH, item)
            dir_items_with_mod_time[item_path] = os.path.getmtime(item_path)

        ''' calling init command second time, checking console output '''
        self.assertFalse(command.run())
        sys.stdout = stdout
        custom_stdout.seek(0)
        expected_content = InitStrings.LIT_INITED + '\n'
        self.assertEqual(expected_content, custom_stdout.read())

        ''' check if files were not modified after calling init command second time '''
        for item in os.listdir(util.TEST_DIR_PATH):
            item_path = os.path.join(util.TEST_DIR_PATH, item)
            self.assertEqual(os.path.getmtime(item_path), dir_items_with_mod_time[item_path])
