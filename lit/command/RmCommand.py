from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.StringManager import StringManager
from lit.command.BaseCommand import BaseCommand
import json
import sys
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
        delete_path = sys.argv[2:][0]

        (filepath, filename) = os.path.split(delete_path)
        (shortname, extension) = os.path.splitext(delete_path)


        if extension == "":
            delete_list = self.get_file_list(delete_path)

            c = open('.lit/tracked_files.json', 'r')
            tracked = json.load(c)
            c.close()


            for file in delete_list:
                if file in tracked['files']:
                    tracked['files'].remove(file)



            b = open('.lit/tracked_files.json', 'w')
            json.dump(tracked, b)
            b.close()

        else:

            a = open('.lit/tracked_files.json', 'r')
            tracked = json.load(a)
            a.close()

            tracked['files'].remove(delete_path)

            b = open('.lit/tracked_files.json', 'w')
            json.dump(tracked, b)
            b.close()




    def get_file_list(self, *args):
        file_list = []
        for root, dirs, files in os.walk(args[0]):
            for f in files:
                path = os.path.join(root, f)
                file_list.append(path)
        return file_list