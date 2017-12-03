import os
import unittest
from lit.file.JSONSerializer import JSONSerializer
from lit.file.CommitsHistoryManager import CommitsHistoryManager

TEST_JSON_FILE_PATH = 'test_json.json'


class TestCommitsHistoryManager(unittest.TestCase):
    commit_message_text_1 = 'Commit message text 1'
    commit_message_text_2 = 'Commit message text 2'

    commit_hash_1 = 'xTrxmrpG393rk4XQ'
    commit_hash_2 = 's6ma2RRPppdeVTpK'

    commit_user_name_1 = 'wbyzku'
    commit_user_name_2 = 'pwdptm'

    commit_user_email_1 = 'urnyxqrd@mail.com'
    commit_user_email_2 = 'mvdtqgjs@mail.com'

    @staticmethod
    def __remove_test_file_if_exists():
        try:
            os.remove(TEST_JSON_FILE_PATH)
        except FileNotFoundError:
            pass

    def setUp(self):
        self.__remove_test_file_if_exists()
        self.serializer = JSONSerializer(TEST_JSON_FILE_PATH)
        CommitsHistoryManager.init(self.serializer)

    def tearDown(self):
        self.__remove_test_file_if_exists()

    def test_write_commit_success(self):
        CommitsHistoryManager.write_commit_info(
            self.commit_message_text_1, self.commit_hash_1, self.commit_user_name_1, self.commit_user_email_1)

        commits = self.serializer.get_all_from_list_item(CommitsHistoryManager.LIST_KEY)
        self.assertEqual(self.commit_message_text_1, commits[0][CommitsHistoryManager.COMMIT_MESSAGE_KEY])

    def test_read_all_commits(self):
        CommitsHistoryManager.write_commit_info(
            self.commit_message_text_1, self.commit_hash_1, self.commit_user_name_1, self.commit_user_email_1)
        CommitsHistoryManager.write_commit_info(
            self.commit_message_text_2, self.commit_hash_2, self.commit_user_name_2, self.commit_user_email_2)

        commits = self.serializer.get_all_from_list_item(CommitsHistoryManager.LIST_KEY)
        self.assertEqual(2, len(commits))
        self.assertEqual(self.commit_message_text_1, commits[0][CommitsHistoryManager.COMMIT_MESSAGE_KEY])
        self.assertEqual(self.commit_hash_1, commits[0][CommitsHistoryManager.COMMIT_HASH_KEY])
        self.assertEqual(self.commit_user_name_1, commits[0][CommitsHistoryManager.COMMIT_USER_NAME_KEY])
        self.assertEqual(self.commit_user_email_1, commits[0][CommitsHistoryManager.COMMIT_USER_EMAIL_KEY])
        self.assertEqual(self.commit_message_text_2, commits[1][CommitsHistoryManager.COMMIT_MESSAGE_KEY])
        self.assertEqual(self.commit_hash_2, commits[1][CommitsHistoryManager.COMMIT_HASH_KEY])
        self.assertEqual(self.commit_user_name_2, commits[1][CommitsHistoryManager.COMMIT_USER_NAME_KEY])
        self.assertEqual(self.commit_user_email_2, commits[1][CommitsHistoryManager.COMMIT_USER_EMAIL_KEY])

    def test_get_commits_count(self):
        CommitsHistoryManager.write_commit_info(
            self.commit_message_text_1, self.commit_hash_1, self.commit_user_name_1, self.commit_user_email_1)
        CommitsHistoryManager.write_commit_info(
            self.commit_message_text_2, self.commit_hash_2, self.commit_user_name_2, self.commit_user_email_2)

        self.assertEqual(2, CommitsHistoryManager.get_commits_count())

    def test_clear_commits_info(self):
        CommitsHistoryManager.write_commit_info(
            self.commit_message_text_1, self.commit_hash_1, self.commit_user_name_1, self.commit_user_email_1)
        CommitsHistoryManager.write_commit_info(
            self.commit_message_text_2, self.commit_hash_2, self.commit_user_name_2, self.commit_user_email_2)

        CommitsHistoryManager._CommitsHistoryManager__clear_commits_info()
        self.assertEqual(0, CommitsHistoryManager.get_commits_count())
