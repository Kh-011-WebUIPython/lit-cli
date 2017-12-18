import os
from tests import util
import zipfile
import unittest

''' Need to run here to change working directory before strings_holder import '''
os.chdir(util.TEST_DIR_PATH)

from lit.strings_holder import AddStrings, RmStrings, TrackedFileSettings, CommitStrings, CommitSettings, LogSettings
from lit.command.AddCommand import AddCommand
from lit.command.RmCommand import RmCommand
from lit.command.InitCommand import InitCommand
from lit.command.CommitCommand import CommitCommand
from lit.command.DiffCommand import DiffCommand
from lit.file.JSONSerializer import JSONSerializer

class TestCommitCommand(unittest.TestCase):
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
        util.clear_dir_content(util.TEST_DIR_PATH)

    def test_files_commit(self):
        CommitCommand().run(**{
            CommitStrings.ARG_MSG_NAME: util.TEST_COMMIT_1_MESSAGE
        })
        commits_history_serializer = JSONSerializer(LogSettings.FILE_PATH)
        commits = commits_history_serializer.get_all_from_list_item(LogSettings.COMMITS_LIST_KEY)
        self.assertEqual(1, len(commits))
        archives = os.listdir(CommitSettings.DIR_PATH)
        self.assertEqual(1, len(archives))
        self.assertEqual(commits[0][CommitSettings.SHORT_HASH] + CommitSettings.ZIP_EXTENSION, archives[0])
        extracted_path = DiffCommand.unzip_commit_snapshot_to_temp_dir(commits[0][CommitSettings.SHORT_HASH])
        extracted_files = os.listdir(extracted_path)
        self.assertEqual(2, len(extracted_files))
        self.assertIn(util.TEST_FILE_1_NAME, extracted_files)
        self.assertIn(util.TEST_FILE_2_NAME, extracted_files)
