from lit.command.BaseCommand import BaseCommand
from zipfile import *
from datetime import datetime
import json
import sys
import os
from hashlib import blake2b
from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.StringManager import StringManager


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

        a = open('.lit/tracked_files.json', 'r')
        tracked = json.load(a)
        a.close()

        file_count = len(os.listdir('.lit/commits/'))
        with ZipFile('.lit/commits/hash' + str(file_count) + '.zip', 'w') as myzip:
            for file in tracked['files']:
                myzip.write(file)


        commit = {
            'user': 'WIP',
                  'long_hash': blake2b(b'Hello world').hexdigest(),
                  'short_hash':  blake2b(b'Hello world').hexdigest()[:10],
                  'datetime': str(datetime.utcnow()),
                  'comment': sys.argv[2:],
                  }

        myzip.close()

        b = open('.lit/commits_log.json', 'r')
        logs = json.load(b)
        b.close()

        c = open('.lit/commits_log.json', 'w')
        logs["commits"].append(commit)
        json.dump(logs, c)

