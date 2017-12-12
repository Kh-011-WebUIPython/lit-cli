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
        if not super().run():
            return False

        serializer_tracked = JSONSerializer(TrackedFileSettings.PATH)
        tracked = serializer_tracked.read_all_items()
        if len(tracked['files']) == 0:
            print('No files in staging area were found')
            return
        zip_file_name = CommitSettings.ZIP_FILE_NAME + CommitSettings.ZIP_EXTENSION

        with ZipFile(zip_file_name, 'w') as myzip:
            files_key = TrackedFileSettings.FILES_KEY
            for file in tracked[files_key]:
                myzip.write(file)

        myzip_hash = self.get_file_hash(myzip.filename)
        os.rename(zip_file_name,
                  zip_file_name[:-8] + str(myzip_hash)[:10] + CommitSettings.ZIP_EXTENSION)
        message = args[CommitStrings.ARG_MSG_NAME]
        commit = {
            CommitSettings.USER: 'user',
            CommitSettings.LONG_HASH: myzip_hash,
            CommitSettings.SHORT_HASH: myzip_hash[:10],
            CommitSettings.DATETIME: str(datetime.utcnow()),
            CommitSettings.COMMENT: message,
        }

        myzip.close()

        serializer_commits = JSONSerializer(LogSettings.PATH)
        logs = serializer_commits.read_all_items()

        c = open(LogSettings.PATH, 'w')
        log_item = LogSettings.KEY
        for item in logs[log_item]:
            if item[CommitSettings.LONG_HASH] == myzip_hash:
                print('There is no changes since last commit')
                json.dump(logs, c)
                c.close()
                return
        logs[log_item].append(commit)
        json.dump(logs, c)
        c.close()
        with open(TrackedFileSettings.PATH, 'r') as file:
            json_data = json.load(file)
        json_data['files'].clear()
        with open(TrackedFileSettings.PATH, 'w') as file:
            json.dump(json_data, file)

    def get_file_hash(self, file_name):
        hsh = hashlib.sha256()
        with open(file_name, 'br') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                hsh.update(chunk)
        return hsh.hexdigest()
