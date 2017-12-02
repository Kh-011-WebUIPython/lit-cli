from lit.command.BaseCommand import BaseCommand
from zipfile import *
from datetime import datetime
import json
import sys
import os


class CommitCommand(BaseCommand):
    def __init__(self, name, help_message):
        super().__init__(name, help_message)

    def run(self, **args):

        a = open('.lit/tracked_files.json', 'r')
        tracked = json.load(a)
        a.close()

        file_count = len(os.listdir('.lit/commits/'))
        with ZipFile('.lit/commits/hash' + str(file_count) + '.zip', 'w') as myzip:
            for file in tracked['files']:
                myzip.write(file)
        myzip.close()

        commit = {
            'user': 'WIP',
                  'long_hash': 'hash()',
                  'short_hash': 'hash()',
                  'datetime': str(datetime.utcnow()),
                  'comment': sys.argv[2:],
                  }

        b = open('.lit/commits_log.json', 'r')
        logs = json.load(b)
        b.close()

        c = open('.lit/commits_log.json', 'w')
        logs["commits"].append(commit)
        json.dump(logs, c)



# if not super().run():
#            return False
#        raise NotImplementedError()
