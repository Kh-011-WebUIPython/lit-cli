from zipfile import *
from datetime import datetime
import json
import os
from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.StringManager import StringManager
from lit.file.SettingsManager import SettingsManager
from lit.file.JSONSerializer import JSONSerializer
import hashlib


class CommitCommand(BaseCommand):
    __COMMAND_COMMIT_NAME_KEY = 'COMMAND_COMMIT_NAME'
    __COMMAND_COMMIT_HELP_KEY = 'COMMAND_COMMIT_HELP'
    __COMMAND_COMMIT_ARGUMENT_MESSAGE_NAME_KEY = 'COMMAND_COMMIT_ARGUMENT_MESSAGE_NAME'
    __COMMAND_COMMIT_ARGUMENT_MESSAGE_HELP_KEY = 'COMMAND_COMMIT_ARGUMENT_MESSAGE_HELP'

    def __init__(self):
        name = StringManager.get_string(self.__COMMAND_COMMIT_NAME_KEY)
        help_message = StringManager.get_string(self.__COMMAND_COMMIT_HELP_KEY)
        arguments = [
            CommandArgument(
                name=StringManager.get_string(self.__COMMAND_COMMIT_ARGUMENT_MESSAGE_NAME_KEY),
                type=str,
                help=StringManager.get_string(self.__COMMAND_COMMIT_ARGUMENT_MESSAGE_HELP_KEY)
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **args):

        serializer_tracked = JSONSerializer(SettingsManager.get_var_value('TRACKED_FILE_PATH'))
        tracked = serializer_tracked.read_all_items()

        file_count = len(os.listdir(SettingsManager.get_var_value('COMMIT_FILES_IN_COMMIT_DIR')))
        with ZipFile(SettingsManager.get_var_value('COMMIT_ZIP_FILE_NAME') + str(file_count) +
                             SettingsManager.get_var_value('COMMIT_ZIP_EXTENCION'), 'w') as myzip:
            for file in tracked['files']:
                myzip.write(file)

        myzip_hash = self.get_file_hash(myzip.filename)
        commit = {
            SettingsManager.get_var_value('COMMIT_USER'): 'WIP',
            SettingsManager.get_var_value('COMMIT_LONG_HASH'): myzip_hash,
            SettingsManager.get_var_value('COMMIT_SHORT_HASH'): myzip_hash[:10],
            SettingsManager.get_var_value('COMMIT_DATETIME'): str(datetime.utcnow()),
            SettingsManager.get_var_value('COMMIT_COMMENT'): args['message'],
        }

        myzip.close()

        serializer_commits = JSONSerializer(SettingsManager.get_var_value('COMMIT_LOG_PATH'))
        logs = serializer_commits.read_all_items()

        c = open(SettingsManager.get_var_value('COMMIT_LOG_PATH'), 'w')
        logs["commits"].append(commit)
        json.dump(logs, c)
        c.close()

    def get_file_hash(self, file_name):
        hsh = hashlib.sha3_384()
        with open(file_name, 'br') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                hsh.update(chunk)
        return hsh.hexdigest()
