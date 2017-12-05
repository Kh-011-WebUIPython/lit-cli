"""
    Run only if strings file is absent or needs an update
"""
from lit.file.JSONSerializer import JSONSerializer
from lit.file.StringManager import StringManager
import lit.paths

STRINGS = {
    'PROGRAM_NAME': 'lit',
    'PROGRAM_DESCRIPTION': 'LIT version control system',

    'COMMAND_ADD_NAME': 'add',
    'COMMAND_ADD_HELP': 'adds files to staging area',
    'COMMAND_ADD_ARGUMENT_PATH_NAME': 'path',
    'COMMAND_ADD_ARGUMENT_PATH_HELP': 'path to file',

    'COMMAND_COMMIT_NAME': 'commit',
    'COMMAND_COMMIT_HELP': 'commits files from staging area to repository',
    'COMMAND_COMMIT_ARGUMENT_MESSAGE_NAME': 'message',
    'COMMAND_COMMIT_ARGUMENT_MESSAGE_HELP': 'message which describes commit',

    'COMMAND_DIFF_NAME': 'diff',
    'COMMAND_DIFF_HELP': 'shows difference between two files',
    'COMMAND_DIFF_ARGUMENT_PATH_1_NAME': 'first',
    'COMMAND_DIFF_ARGUMENT_PATH_1_HELP': 'path to first file',
    'COMMAND_DIFF_ARGUMENT_PATH_2_NAME': 'second',
    'COMMAND_DIFF_ARGUMENT_PATH_2_HELP': 'path to second file',

    'COMMAND_INIT_NAME': 'init',
    'COMMAND_INIT_HELP': 'initializes repository in the current directory',

    'COMMAND_LOG_NAME': 'log',
    'COMMAND_LOG_HELP': 'shows lit log',

    'COMMAND_RM_NAME': 'rm',
    'COMMAND_RM_HELP': 'removes files from staging area',
    'COMMAND_RM_ARGUMENT_PATH_NAME': 'path',
    'COMMAND_RM_ARGUMENT_PATH_HELP': 'path to file',

    'COMMAND_STATUS_NAME': 'status',
    'COMMAND_STATUS_HELP': 'shows repository state',
}

if __name__ == '__main__':
    strings_serializer = JSONSerializer(lit.paths.STRINGS_PATH)
    StringManager.init(strings_serializer)
    StringManager.set_strings(STRINGS)