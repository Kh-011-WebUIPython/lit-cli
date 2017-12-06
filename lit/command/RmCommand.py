from lit.command.BaseCommand import  CommandArgument
from lit.file.StringManager import StringManager
from lit.command.BaseCommand import BaseCommand
from lit.file.JSONSerializer import JSONSerializer
from lit.file.SettingsManager import SettingsManager
import json
import os


class RmCommand(BaseCommand):
    __COMMAND_RM_NAME_KEY = 'COMMAND_RM_NAME'
    __COMMAND_RM_HELP_KEY = 'COMMAND_RM_HELP'
    __COMMAND_RM_ARGUMENT_PATH_NAME_KEY = 'COMMAND_RM_ARGUMENT_PATH_NAME'
    __COMMAND_RM_ARGUMENT_PATH_HELP_KEY = 'COMMAND_RM_ARGUMENT_PATH_HELP'

    def __init__(self):
        name = StringManager.get_string(self.__COMMAND_RM_NAME_KEY)
        help_message = StringManager.get_string(self.__COMMAND_RM_HELP_KEY)
        arguments = [
            CommandArgument(
                name=StringManager.get_string(self.__COMMAND_RM_ARGUMENT_PATH_NAME_KEY),
                type=str,
                help=StringManager.get_string(self.__COMMAND_RM_ARGUMENT_PATH_HELP_KEY)
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **args):

        delete_path = args['path']

        (shortname, extension) = os.path.splitext(delete_path)

        serializer_tracked = JSONSerializer(SettingsManager.get_var_value('TRACKED_FILE_PATH'))
        tracked = serializer_tracked.read_all_items()

        if extension == "":
            delete_list = self.get_file_list(delete_path)

            for file in delete_list:
                if file in tracked['files']:
                    tracked['files'].remove(file)

            b = open(SettingsManager.get_var_value('TRACKED_FILE_PATH'), 'w')
            json.dump(tracked, b)
            b.close()

        else:
            tracked['files'].remove(delete_path)

            b = open(SettingsManager.get_var_value('TRACKED_FILE_PATH'), 'w')
            json.dump(tracked, b)
            b.close()




    def get_file_list(self, *args):
        file_list = []
        for root, dirs, files in os.walk(args[0]):
            for f in files:
                path = os.path.join(root, f)
                file_list.append(path)
        return file_list