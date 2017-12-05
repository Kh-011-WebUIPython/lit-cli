from lit.command.BaseCommand import BaseCommand
import os
import sys
import json
from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.StringManager import StringManager


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

    def run(self, *args):
        file_list = self.get_file_list(sys.argv[2:])
        if not file_list == None:
           a = open('.lit/tracked_files.json', 'r')
           tracked = json.load(a)
           a.close()
           self.save_tracked_files(file_list, tracked)
        else:
            pass

    def get_file_list(self, *args):
        file_list = []
        for root, dirs, files in os.walk(args[0][0]):
            for f in files:
                path = os.path.join(root, f)
                file_list.append(path)
        return file_list

    def save_tracked_files(self, file_list, tracked):

        b = open('.lit/tracked_files.json', 'w')
        for file in file_list:
            if file not in tracked['files']:
                tracked['files'].append(file)
        json.dump(tracked, b)
        b.close()
        pass





