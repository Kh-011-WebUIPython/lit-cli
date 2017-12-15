import os
import shutil

TEST_DIR_PATH = '/tmp/tempramdisk'

TEST_FILE_1_NAME = 'file1.txt'
TEST_FILE_1_PATH = os.path.join(TEST_DIR_PATH, TEST_FILE_1_NAME)
TEST_FILE_1_CONTENT = 'file 1 content'

TEST_FILE_2_NAME = 'file2.txt'
TEST_FILE_2_PATH = os.path.join(TEST_DIR_PATH, TEST_FILE_2_NAME)
TEST_FILE_2_CONTENT = 'file 2 content'

TEST_NONEXISTENT_FILE_NAME = 'file_that_does_not_exist.txt'

TEST_COMMIT_1_MESSAGE = 'test commit 1 message'
TEST_COMMIT_2_MESSAGE = 'test commit 2 message'

def clear_dir_content(dir_path):
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            raise RuntimeError
