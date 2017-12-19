"""
    String constants for lit commands description
"""
import os


class ProgramStrings(object):
    NAME = 'lit'
    DESCRIPTION = 'LIT version control system'


class ProgramSettings(object):
    LIT_WORKING_DIRECTORY_PATH = os.getcwd()
    LIT_DIR = '.lit'
    LIT_PATH = os.path.join(LIT_WORKING_DIRECTORY_PATH, LIT_DIR)
    LIT_SETTINGS_NAME = 'settings.json'
    LIT_SETTINGS_PATH = os.path.join(LIT_PATH, LIT_SETTINGS_NAME)

    ACTIVE_BRANCH_KEY = 'active_branch'
    ACTIVE_BRANCH_DEFAULT = 'master'

    USER_NAME_KEY = 'user_name'
    USER_NAME_DEFAULT = 'user'


class AddStrings(object):
    NAME = 'add'
    HELP = 'add files to staging area'
    ARG_PATH_NAME = 'path'
    ARG_PATH_HELP = 'path to file'


class BranchSettings(object):
    JSON_KEY_NAME = 'branch_name'
    JSON_FILE_NAME_SUFFIX = '_commits_log.json'


class CheckoutStrings(object):
    NAME = 'checkout'
    HELP = 'checkout to another branch'
    ARG_BRANCH_NAME = 'branch'
    ARG_BRANCH_HELP = 'branch name to checkout'


class CheckoutSettings(object):
    pass


class CommitStrings(object):
    NAME = 'commit'
    HELP = 'commit files from staging area to repository'
    ARG_MSG_NAME = 'message'
    ARG_MSG_HELP = 'message which describes commit'


class CommitSettings(object):
    DIR_NAME = 'commits'
    DIR_PATH = os.path.join(ProgramSettings.LIT_PATH, DIR_NAME)
    TEMP_ZIP_FILE_NAME = 'hash'
    TEMP_ZIP_FILE_PATH = os.path.join(DIR_PATH, TEMP_ZIP_FILE_NAME)
    ZIP_EXTENSION = '.zip'
    USER = 'user'
    LONG_HASH = 'long_hash'
    SHORT_HASH = 'short_hash'
    DATETIME = 'datetime'
    MESSAGE = 'message'
    SHORT_HASH_LENGTH = 10


class DiffStrings(object):
    NAME = 'diff'
    HELP = 'show changes in file since last commit'
    ARG_PATH_1_NAME = 'file'
    ARG_PATH_1_HELP = 'path to file'
    ARG_PATH_2_NAME = 'second'
    ARG_PATH_2_HELP = 'path to second file'


class DiffSettings(object):
    TEMP_PATH = os.path.join(ProgramSettings.LIT_PATH, 'temp')


class InitStrings(object):
    NAME = 'init'
    HELP = 'initialize repository in the current directory'
    LIT_INITED = 'LIT repository has been already initialised in this directory'


class InitSettings(object):
    pass


class LogStrings(object):
    NAME = 'log'
    HELP = 'show commits history'
    COMMITS_NOT_FOUND = 'No commits were found'


class LogSettings(object):
    COMMIT_STR_NAME = 'Commit:'
    COMMIT_MESSAGE_STR_NAME = 'Commit message:'
    COMMIT_USERNAME_STR_NAME = 'Username:'
    COMMIT_DATE_STR_NAME = 'Date:'
    FILE_NAME = 'commits_log.json'
    FILE_PATH = os.path.join(ProgramSettings.LIT_PATH, FILE_NAME)
    INIT_CONTENT = '{"commits":[]}'
    COMMITS_LIST_KEY = 'commits'
    MESSAGE_FORMAT = COMMIT_STR_NAME + ' {0}' + os.linesep \
                     + COMMIT_MESSAGE_STR_NAME + ' {1}' + os.linesep \
                     + COMMIT_USERNAME_STR_NAME + ' {2}' + os.linesep \
                     + COMMIT_DATE_STR_NAME + ' {3}' + os.linesep


class RmStrings(object):
    NAME = 'rm'
    HELP = 'remove files from staging area'
    ARG_PATH_NAME = 'path'
    ARG_PATH_HELP = 'path to file'


class StatusStrings(object):
    NAME = 'status'
    HELP = 'show repository state'


class TrackedFileSettings(object):
    FILE_NAME = 'tracked_files.json'
    FILE_PATH = os.path.join(ProgramSettings.LIT_PATH, FILE_NAME)
    FILES_KEY = 'files'
    INIT_CONTENT = '{"files": []}'
