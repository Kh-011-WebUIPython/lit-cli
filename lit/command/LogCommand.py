from lit.command.BaseCommand import BaseCommand
from lit.file.StringManager import StringManager
from lit.file.SettingsManager import SettingsManager
from lit.file.JSONSerializer import JSONSerializer

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

        serializer = JSONSerializer(SettingsManager.get_var_value('COMMIT_LOG_PATH'))
        logs = serializer.read_all_items()
        json_commit_print(logs)





def json_commit_print(json):
    for commit in json["commits"]:
        s = SettingsManager.get_var_value('LOG_COMMIT') + commit["short_hash"]+ ";\n" +\
            SettingsManager.get_var_value('LOG_COMMIT_MESSAGE') + commit["comment"] + ";\n" + \
            SettingsManager.get_var_value('LOG_USERNAME') + commit["user"] + ";\n" + \
            SettingsManager.get_var_value('LOG_DATE') + commit["datetime"][:19] + "\n"
        print(s)
