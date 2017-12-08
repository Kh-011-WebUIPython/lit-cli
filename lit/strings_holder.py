"""
    String constants for lit commands description
"""
from enum import Enum
class StringsHolder(Enum):
    class Program:
        NAME = 'lit';
        DESCRIPTION = 'LIT version control system';
    class Commands:
        class Add(Enum):
            NAME = 'add';
            HELP = 'adds files to staging area';
            class Arguments(Enum):
                PATH_NAME = 'path';
                PATH_HELP = 'path to file';
        class Commit(Enum):
            NAME = 'commit';
            HELP = 'commits files from staging area to repository';
            class Arguments(Enum):
                MSG_NAME = 'message';
                MSG_HELP = 'message which describes commit';
        class Diff(Enum):
            NAME = 'diff';
            HELP = 'adds files to staging area';
            class Arguments(Enum):
                PATH_1_NAME = 'first';
                PATH_1_HELP = 'path to first file';
                PATH_2_NAME = 'second';
                PATH_2_HELP = 'path to second file';
        class Init(Enum):
            NAME = 'init';
            HELP = 'initializes repository in the current directory';
        class Log(Enum):
            NAME = 'log';
            HELP = 'shows lit log';
        class Rm(Enum):
            NAME = 'rm';
            HELP = 'removes files from staging area';
            class Arguments(Enum):
                PATH_NAME = 'path';
                PATH_HELP = 'path to file';
        class Status(Enum):
            NAME = 'status';
            HELP = 'shows repository state';
    class Settings(Enum):
        TRACKED_FILE_PATH = '.lit/tracked_files.json';
        COMMIT_LOG_PATH = '.lit/commits_log.json';
        class Log(Enum):
            COMMIT = 'Commit: ';
            COMMIT_MESSAGE = 'Commit message: ';
            USERNAME = 'Username: ';
            DATE = 'Date: ';
        class Init(Enum):
            LIT = '.lit';
            LIT_INITED = 'LIT has been already inited in this directory';
            COMMIT_DIR = 'commits';
            TRACKED_FILE = 'tracked_files.json';
            COMMIT_LOG = 'commits_log.json';
            TRACKED_FILE_INIT = '{"files": []}';
            COMMIT_LOG_INIT = '{"commits":[]}';
        class Commit(Enum):
            FILES_IN_COMMIT_DIR = '.lit/commits/';
            ZIP_FILE_NAME = '.lit/commits/hash';
            ZIP_EXTENCION = '.zip';
            USER = 'user';
            LONG_HASH = 'long_hash';
            SHORT_HASH = 'short_hash';
            DATETIME = 'datetime';
            COMMENT = 'comment';
