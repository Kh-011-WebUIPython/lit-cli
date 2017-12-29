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


class BranchStrings(object):
    NAME = 'branch'
    HELP = 'manage branch'

    ARG_NAME_NAME = 'name'
    ARG_NAME_HELP = 'branch name'

    ARG_ACTION_NAME = 'action'
    ARG_ACTION_HELP = 'action to perform with branch'
    ARG_ACTION_CHOICE_CREATE = 'create'
    ARG_ACTION_CHOICE_DELETE = 'delete'


class BranchSettings(object):
    JSON_KEY_NAME = 'branch_name'
    JSON_FILE_NAME_SUFFIX = '_commits_log.json'


class CheckoutStrings(object):
    NAME = 'checkout'
    HELP = 'checkout to another branch'
    ARG_BRANCH_NAME = 'branch'
    ARG_BRANCH_HELP = 'branch name to checkout'


class CheckoutSettings(object):
    TEMP_DIR_NAME = 'checkout_temp'
    TEMP_DIR_PATH = os.path.join(ProgramSettings.LIT_PATH, TEMP_DIR_NAME)


class CommitStrings(object):
    NAME = 'commit'
    HELP = 'commit files from staging area to repository'
    ARG_MSG_NAME = 'message'
    ARG_MSG_HELP = 'message which describes commit'


class CommitSettings(object):
    DIR_NAME = 'commits'
    DIR_PATH = os.path.join(ProgramSettings.LIT_PATH, DIR_NAME)
    TEMP_FILE_NAME = 'hash'
    TEMP_FILE_PATH = os.path.join(DIR_PATH, TEMP_FILE_NAME)
    FILE_EXTENSION = '.zip'

    USER_KEY = 'user'
    LONG_HASH_KEY = 'long_hash'
    DATETIME_KEY = 'datetime'
    MESSAGE_KEY = 'message'
    FILES_KEY = 'files'
    FILES_PATH_KEY = 'path'
    FILES_FILE_HASH_KEY = 'file_hash'
    FILES_COMMIT_HASH_KEY = 'commit_hash'

    SHORT_HASH_LENGTH = 10

    TEMP_DIR_NAME = 'temp'
    TEMP_DIR_PATH = os.path.join(ProgramSettings.LIT_PATH, TEMP_DIR_NAME)


class CommandStrings(object):
    RUN_METHOD_ERROR_MESSAGE = 'Command completed with errors'


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
    COMMIT_MESSAGE_STR_NAME = 'Message:'
    COMMIT_USERNAME_STR_NAME = 'Username:'
    COMMIT_DATE_STR_NAME = 'Date:'
    COMMIT_HASH_STR_NAME = 'Hash:'
    FILE_NAME = 'commits_log.json'
    FILE_PATH = os.path.join(ProgramSettings.LIT_PATH, FILE_NAME)
    INIT_CONTENT = '{"commits":[]}'
    COMMITS_LIST_KEY = 'commits'
    MESSAGE_FORMAT = ' > ' + '{0: <8}'.format(COMMIT_HASH_STR_NAME) + ' {0}' + os.linesep + \
                     '   ' + '{0: <8}'.format(COMMIT_MESSAGE_STR_NAME) + ' {1}' + os.linesep + \
                     '   ' + '{0: <8}'.format(COMMIT_DATE_STR_NAME) + ' {3}'


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
