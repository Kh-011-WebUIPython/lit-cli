from lit.command.BaseCommand import BaseCommand
from lit.file.StringManager import StringManager
from lit.file.SettingsManager import SettingsManager
import json


class StatusCommand(BaseCommand):
    __COMMAND_STATUS_NAME_KEY = 'COMMAND_STATUS_NAME'
    __COMMAND_STATUS_HELP_KEY = 'COMMAND_STATUS_HELP'

    def __init__(self):
        name = StringManager.get_string(self.__COMMAND_STATUS_NAME_KEY)
        help_message = StringManager.get_string(self.__COMMAND_STATUS_HELP_KEY)
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        if not super().run():
            return False
        with open(SettingsManager.get_var_value('TRACKED_FILE_PATH'), 'r') as file:
            json_data = json.load(file)
        print('Files in staging area:')
        print(*json_data['files'], sep='\n')
