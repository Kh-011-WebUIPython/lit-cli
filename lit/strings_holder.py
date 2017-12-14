"""
    String constants for lit commands description
"""
import os
import lit.paths


class ProgramStrings(object):
    NAME = 'lit'
    DESCRIPTION = 'LIT version control system'


class AddStrings(object):
    NAME = 'add'
    HELP = 'add files to staging area'
    ARG_PATH_NAME = 'path'
    ARG_PATH_HELP = 'path to file'


class CommitStrings(object):
    NAME = 'commit'
    HELP = 'commit files from staging area to repository'
    ARG_MSG_NAME = 'message'
    ARG_MSG_HELP = 'message which describes commit'


class DiffStrings(object):
    NAME = 'diff'
    HELP = 'show changes in file since last commit'
    ARG_PATH_1_NAME = 'file'
    ARG_PATH_1_HELP = 'path to file'
    ARG_PATH_2_NAME = 'second'
    ARG_PATH_2_HELP = 'path to second file'


class InitStrings(object):
    NAME = 'init'
    HELP = 'initialize repository in the current directory'


class LogStrings(object):
    NAME = 'log'
    HELP = 'show commits history'


class RmStrings(object):
    NAME = 'rm'
    HELP = 'remove files from staging area'
    ARG_PATH_NAME = 'path'
    ARG_PATH_HELP = 'path to file'


class StatusStrings(object):
    NAME = 'status'
    HELP = 'show repository state'


class InitSettings(object):
    LIT_DIR = '.lit'
    LIT_PATH = os.path.join(os.getcwd(), LIT_DIR)
    LIT_INITED = 'LIT has been already inited in this directory'


class DiffSettings(object):
    TEMP_PATH = os.path.join(InitSettings.LIT_PATH, 'temp')


class TrackedFileSettings(object):
    PATH = '.lit/tracked_files.json'
    FILE_NAME = 'tracked_files.json'
    FILES_KEY = 'files'
    INIT_CONTENT = '{"files": []}'


class LogSettings(object):
    COMMIT = 'Commit: '
    COMMIT_MESSAGE = 'Commit message: '
    USERNAME = 'Username: '
    DATE = 'Date: '
    PATH = '.lit/commits_log.json'
    FILE_NAME = 'commits_log.json'
    INIT_CONTENT = '{"commits":[]}'
    KEY = "commits"


class CommitSettings(object):
    DIR_PATH = '.lit/commits/'
    DIR_NAME = 'commits'
    ZIP_FILE_NAME = '.lit/commits/hash'
    ZIP_EXTENSION = '.zip'
    USER = 'user'
    LONG_HASH = 'long_hash'
    SHORT_HASH = 'short_hash'
    DATETIME = 'datetime'
    COMMENT = 'comment'
