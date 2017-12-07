import os
import json
from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.StringManager import StringManager
from lit.file.SettingsManager import SettingsManager
from lit.file.JSONSerializer import JSONSerializer


class AddCommand(BaseCommand):
    __COMMAND_ADD_NAME_KEY = 'COMMAND_ADD_NAME'
    __COMMAND_ADD_HELP_KEY = 'COMMAND_ADD_HELP'
    __COMMAND_ADD_ARGUMENT_PATH_NAME_KEY = 'COMMAND_ADD_ARGUMENT_PATH_NAME'
    __COMMAND_ADD_ARGUMENT_PATH_HELP_KEY = 'COMMAND_ADD_ARGUMENT_PATH_HELP'

    def __init__(self):
        name = StringManager.get_string(self.__COMMAND_ADD_NAME_KEY)
        help_message = StringManager.get_string(self.__COMMAND_ADD_HELP_KEY)
        arguments = [
            CommandArgument(
                name=StringManager.get_string(self.__COMMAND_ADD_ARGUMENT_PATH_NAME_KEY),
                type=str,
                help=StringManager.get_string(self.__COMMAND_ADD_ARGUMENT_PATH_HELP_KEY)
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **args):


        file_list = self.get_file_list(args['path'])
        if file_list == []:
            file_list = self.get_file(args['path'])
        else:
            pass



        if not file_list == None:
            serializer = JSONSerializer(SettingsManager.get_var_value('TRACKED_FILE_PATH'))
            tracked = serializer.read_all_items()
            self.save_tracked_files(file_list, tracked)

        else:
            pass

    def get_file_list(self, *args):
        file_list = []
        for root, dirs, files in os.walk(args[0]):
            for f in files:
                path = os.path.join(root, f)
                file_list.append(path)

        return file_list

    def get_file(self,*args):
        file_list = []
        path = os.path.join(args[0])
        file_list.append(path)
        return file_list

    def save_tracked_files(self, file_list, tracked):
        b = open(SettingsManager.get_var_value('TRACKED_FILE_PATH'), 'w')
        for file in file_list:
            if file not in tracked['files']:
                tracked['files'].append(file)
        json.dump(tracked, b)
        b.close()
        pass
