from lit.command.BaseCommand import BaseCommand
from lit.file.StringManager import StringManager

import json

class LogCommand(BaseCommand):
    __COMMAND_LOG_NAME_KEY = 'COMMAND_LOG_NAME'
    __COMMAND_LOG_HELP_KEY = 'COMMAND_LOG_HELP'

    def __init__(self):
        name = StringManager.get_string(self.__COMMAND_LOG_NAME_KEY)
        help_message = StringManager.get_string(self.__COMMAND_LOG_HELP_KEY)
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        b = open('.lit/commits_log.json', 'r')
        logs = json.load(b)
        json_commit_print(logs)
        b.close()




def json_commit_print(json):
    for commit in json["commits"]:
        s = "Commit: " + commit["short_hash"]+ ";\n" +\
            "Commit message: " + commit["comment"][0] + ";\n" + \
            "Username: " + commit["user"] + ";\n" + \
            "Date: " + commit["datetime"][:19] + "\n"
        print(s)
