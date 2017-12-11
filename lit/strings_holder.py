"""
    String constants for lit commands description
"""
from enum import Enum


class ProgramStrings(Enum):
    NAME = 'lit'
    DESCRIPTION = 'LIT version control system'


class AddStrings(Enum):
    NAME = 'add'
    HELP = 'adds files to staging area'
    ARG_PATH_NAME = 'path'
    ARG_PATH_HELP = 'path to file'


class CommitStrings(Enum):
    NAME = 'commit'
    HELP = 'commits files from staging area to repository'
    ARG_MSG_NAME = 'message'
    ARG_MSG_HELP = 'message which describes commit'


class DiffStrings(Enum):
    NAME = 'diff'
    HELP = 'adds files to staging area'
    ARG_PATH_1_NAME = 'first'
    ARG_PATH_1_HELP = 'path to first file'
    ARG_PATH_2_NAME = 'second'
    ARG_PATH_2_HELP = 'path to second file'


class InitStrings(Enum):
    NAME = 'init'
    HELP = 'initializes repository in the current directory'


class LogStrings(Enum):
    NAME = 'log'
    HELP = 'shows lit log'


class RmStrings(Enum):
    NAME = 'rm'
    HELP = 'removes files from staging area'
    ARG_PATH_NAME = 'path'
    ARG_PATH_HELP = 'path to file'


class StatusStrings(Enum):
    NAME = 'status'
    HELP = 'shows repository state'


class InitSettings(Enum):
    LIT_DIR = '.lit'
    LIT_INITED = 'LIT has been already inited in this directory'


class TrackedFileSettings(Enum):
    PATH = '.lit/tracked_files.json'
    FILE_NAME = 'tracked_files.json'
    FILES_KEY = 'files'
    INIT_CONTENT = '{"files": []}'


class LogSettings(Enum):
    COMMIT = 'Commit: '
    COMMIT_MESSAGE = 'Commit message: '
    USERNAME = 'Username: '
    DATE = 'Date: '
    PATH = '.lit/commits_log.json'
    FILE_NAME = 'commits_log.json'
    INIT_CONTENT = '{"commits":[]}'
    KEY = "commits"


class CommitSettings(Enum):
    DIR_PATH = '.lit/commits/'
    DIR_NAME = 'commits'
    ZIP_FILE_NAME = '.lit/commits/hash'
    ZIP_EXTENSION = '.zip'
    USER = 'user'
    LONG_HASH = 'long_hash'
    SHORT_HASH = 'short_hash'
    DATETIME = 'datetime'
    COMMENT = 'comment'
