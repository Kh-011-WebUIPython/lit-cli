import sys
import os
import io
import unittest

from tests import util

''' Need to run here to change working directory before strings_holder import '''
os.chdir(util.TEST_DIR_PATH)

from lit.strings_holder import LogStrings, LogSettings, AddStrings, CommitStrings, CommitSettings
from lit.command.LogCommand import LogCommand
from lit.command.InitCommand import InitCommand
from lit.command.AddCommand import AddCommand
from lit.command.CommitCommand import CommitCommand
from lit.file.JSONSerializer import JSONSerializer
import lit.util


class TestLogCommand(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        sys.stdout = self.stdout
        lit.util.clear_dir_content(util.TEST_DIR_PATH)

    def test_output_for_one_commit(self):
        InitCommand().run()
        self.create_test_file()
        AddCommand().run(**{
            AddStrings.ARG_PATH_NAME: util.TEST_FILE_1_NAME
        })
        CommitCommand().run(**{
            CommitStrings.ARG_MSG_NAME: util.TEST_COMMIT_1_MESSAGE
        })
        LogCommand().run()
        serializer = JSONSerializer(lit.util.get_current_branch_log_file_path())
        commits = serializer.get_all_from_list_item(LogSettings.COMMITS_LIST_KEY)
        self.assertEqual(1, len(commits))
        commit_short_hash = commits[0][CommitSettings.LONG_HASH][:CommitSettings.SHORT_HASH_LENGTH]
        commit_message = commits[0][CommitSettings.MESSAGE]
        commit_user = commits[0][CommitSettings.USER]
        commit_datetime = commits[0][CommitSettings.DATETIME]
        expected_output = LogSettings.MESSAGE_FORMAT.format(
            commit_short_hash, commit_message, commit_user, commit_datetime) + os.linesep
        actual_output = self.get_stdout_content()
        self.assertEqual(expected_output, actual_output,
                         ('expected:' + os.linesep + '{0}' + os.linesep +
                          'actual:' + os.linesep + '{1}')
                         .format(expected_output, actual_output))

    def test_output_if_no_commits_were_made(self):
        InitCommand().run()
        LogCommand().run()
        expected_output = LogStrings.COMMITS_NOT_FOUND + os.linesep
        actual_output = self.get_stdout_content()
        self.assertEqual(expected_output, actual_output)

    @staticmethod
    def get_stdout_content():
        sys.stdout.seek(0)
        return sys.stdout.read()

    @staticmethod
    def create_test_file():
        with open(util.TEST_FILE_1_PATH, 'w') as file:
            file.write(util.TEST_FILE_1_CONTENT)
