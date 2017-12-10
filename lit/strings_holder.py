"""
    String constants for lit commands description
"""
from enum import Enum


class StringsHolder(Enum):
    class Program:
        NAME = 'lit'
        DESCRIPTION = 'LIT version control system'

    class Commands:
        class Add(Enum):
            NAME = 'add'
            HELP = 'adds files to staging area'

            class Arguments(Enum):
                PATH_NAME = 'path'
                PATH_HELP = 'path to file'

        class Commit(Enum):
            NAME = 'commit'
            HELP = 'commits files from staging area to repository'

            class Arguments(Enum):
                MSG_NAME = 'message'
                MSG_HELP = 'message which describes commit'

        class Diff(Enum):
            NAME = 'diff'
            HELP = 'adds files to staging area'

            class Arguments(Enum):
                PATH_1_NAME = 'first'
                PATH_1_HELP = 'path to first file'
                PATH_2_NAME = 'second'
                PATH_2_HELP = 'path to second file'

        class Init(Enum):
            NAME = 'init'
            HELP = 'initializes repository in the current directory'

        class Log(Enum):
            NAME = 'log'
            HELP = 'shows lit log'

        class Rm(Enum):
            NAME = 'rm'
            HELP = 'removes files from staging area'

            class Arguments(Enum):
                PATH_NAME = 'path'
                PATH_HELP = 'path to file'

        class Status(Enum):
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
