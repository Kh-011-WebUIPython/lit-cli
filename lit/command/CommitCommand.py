import hashlib
import json
import os
from datetime import datetime
from zipfile import *

from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.JSONSerializer import JSONSerializer
import hashlib
import lit.paths
from lit.strings_holder import CommitStrings, TrackedFileSettings, CommitSettings, LogSettings


class CommitCommand(BaseCommand):
    def __init__(self):
        name = CommitStrings.NAME
        help_message = CommitStrings.HELP
        arguments = [
            CommandArgument(
                name=CommitStrings.ARG_MSG_NAME,
                type=str,
                help=CommitStrings.ARG_MSG_HELP
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **args):

        serializer_tracked = JSONSerializer(TrackedFileSettings.PATH)
        tracked = serializer_tracked.read_all_items()


        file_count = len(os.listdir(CommitSettings.DIR_PATH.value))
        with ZipFile(CommitSettings.ZIP_FILE_NAME + str(file_count) +
                     CommitSettings.ZIP_EXTENSION, 'w') as myzip:
            files_key = TrackedFileSettings.FILES_KEY
            for file in tracked[files_key]:
                myzip.write(file)

        myzip_hash = self.get_file_hash(myzip.filename)
        message = CommitStrings.Arguments.MSG_NAME.value
        commit = {
            CommitSettings.USER: 'WIP',
            CommitSettings.LONG_HASH: myzip_hash,
            CommitSettings.COMMIT_SHORT_HASH: myzip_hash[:10],
            CommitSettings.DATETIME: str(datetime.utcnow()),
            CommitSettings.COMMENT: args[message],
        }

        myzip.close()

        serializer_commits = JSONSerializer(CommitSettings.LOG_PATH)
        logs = serializer_commits.read_all_items()

        c = open(CommitSettings.LOG_PATH, 'w')
        log_item = LogSettings.KEY
        logs[log_item].append(commit)
        json.dump(logs, c)
        c.close()
        with open(SettingsManager.get_var_value('TRACKED_FILE_PATH'), 'r') as file:
            json_data = json.load(file)
        json_data['files'].clear()
        with open(SettingsManager.get_var_value('TRACKED_FILE_PATH'), 'w') as file:
            json.dump(json_data, file)

    def get_file_hash(self, file_name):
        hsh = hashlib.sha256()
        with open(file_name, 'br') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                hsh.update(chunk)
        return hsh.hexdigest()
