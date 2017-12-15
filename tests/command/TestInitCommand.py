import sys
import os
import io
import unittest
from lit.command.InitCommand import InitCommand
from lit.strings_holder import ProgramSettings, InitSettings, TrackedFileSettings, LogSettings, CommitSettings
import tests.util


class TestInitCommand(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ProgramSettings.LIT_PATH = os.path.join(tests.util.TEST_DIR_PATH, ProgramSettings.LIT_DIR)

    def setUp(self):
        if not os.path.isdir(tests.util.TEST_DIR_PATH):
            raise EnvironmentError('Could not find test dir \'' + tests.util.TEST_DIR_PATH + '\'')
        if len(os.listdir(tests.util.TEST_DIR_PATH)) != 0:
            tests.util.clear_dir_content(tests.util.TEST_DIR_PATH)

    def tearDown(self):
        tests.util.clear_dir_content(tests.util.TEST_DIR_PATH)

    def test_check_dot_lit_dir_content(self):
        InitCommand().run()
        lit_path = os.path.join(tests.util.TEST_DIR_PATH, ProgramSettings.LIT_DIR)
        self.assertTrue(os.path.isdir(lit_path), lit_path)
        expected_files = {TrackedFileSettings.FILE_NAME, LogSettings.FILE_NAME}
        expected_dirs = {CommitSettings.DIR_NAME}
        dir_items = os.listdir(lit_path)
        self.assertEqual(3, len(dir_items))
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
        command.run()

        ''' saving repo settings files' last modification timestamps '''
        dir_items_with_mod_time = {}
        for item in os.listdir(tests.util.TEST_DIR_PATH):
            item_path = os.path.join(tests.util.TEST_DIR_PATH, item)
            dir_items_with_mod_time[item_path] = os.path.getmtime(item_path)

        ''' calling init command second time, checking console output '''
        command.run()
        sys.stdout = stdout
        custom_stdout.seek(0)
        expected_content = InitSettings.LIT_INITED + '\n'
        self.assertEqual(expected_content, custom_stdout.read())

        ''' check if files were not modified after calling init command second time '''
        for item in os.listdir(tests.util.TEST_DIR_PATH):
            item_path = os.path.join(tests.util.TEST_DIR_PATH, item)
            self.assertEqual(os.path.getmtime(item_path), dir_items_with_mod_time[item_path])
