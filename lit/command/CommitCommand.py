import hashlib
import json
import os
from datetime import datetime
from zipfile import *

from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import StringsHolder


class CommitCommand(BaseCommand):
    def __init__(self):
        name = StringsHolder.Commands.Commit.NAME
        help_message = StringsHolder.Commands.Commit.HELP
        arguments = [
            CommandArgument(
                name=StringsHolder.Commands.Commit.Arguments.MSG_NAME,
                type=str,
                help=StringsHolder.Commands.Commit.Arguments.MSG_HELP
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **args):

        serializer_tracked = JSONSerializer(StringsHolder.TrackedFileSettings.PATH)
        tracked = serializer_tracked.read_all_items()

        file_count = len(os.listdir(StringsHolder.CommitSettings.DIR_PATH.value))
        with ZipFile(StringsHolder.CommitSettings.ZIP_FILE_NAME + str(file_count) +
                     StringsHolder.CommitSettings.ZIP_EXTENSION, 'w') as myzip:
            files_key = StringsHolder.TrackedFileSettings.FILES_KEY
            for file in tracked[files_key]:
                myzip.write(file)

        myzip_hash = self.get_file_hash(myzip.filename)
        message = StringsHolder.Commands.Commit.Arguments.MSG_NAME.value
        commit = {
            StringsHolder.CommitSettings.USER: 'WIP',
            StringsHolder.CommitSettings.LONG_HASH: myzip_hash,
            StringsHolder.CommitSettings.COMMIT_SHORT_HASH: myzip_hash[:10],
            StringsHolder.CommitSettings.DATETIME: str(datetime.utcnow()),
            StringsHolder.CommitSettings.COMMENT: args[message],
        }

        myzip.close()

        serializer_commits = JSONSerializer(StringsHolder.CommitSettings.LOG_PATH)
        logs = serializer_commits.read_all_items()

        c = open(StringsHolder.CommitSettings.LOG_PATH, 'w')
        log_item = StringsHolder.LogSettings.KEY
        logs[log_item].append(commit)
        json.dump(logs, c)
        c.close()

    def get_file_hash(self, file_name):
        hsh = hashlib.sha3_384()
        with open(file_name, 'br') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                hsh.update(chunk)
        return hsh.hexdigest()
