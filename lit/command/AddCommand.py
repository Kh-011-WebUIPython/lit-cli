import json
import os

from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import StringsHolder


class AddCommand(BaseCommand):

    def __init__(self):
        name = StringsHolder.Commands.Add.NAME
        help_message = StringsHolder.Commands.Add.HELP
        arguments = [
            CommandArgument(
                name=StringsHolder.Commands.Add.Arguments.PATH_NAME,
                type=str,
                help=StringsHolder.Commands.Add.Arguments.PATH_HELP
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        path = StringsHolder.Commands.Add.Arguments.PATH_NAME.value
        file_list = self.get_file_list(args[path])
        if file_list == []:
            file_list = self.get_file(args[path])
        else:
            pass

        if file_list == None:
            serializer = JSONSerializer(StringsHolder.TrackedFileSettings.PATH)
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

    def get_file(self, *args):
        file_list = []
        path = os.path.join(args[0])
        file_list.append(path)
        return file_list

    def save_tracked_files(self, file_list, tracked):
        b = open(StringsHolder.TrackedFileSettings.PATH.value, 'w')
        for file in file_list:
            files_key = StringsHolder.TrackedFileSettings.FILES_KEY
            if file not in tracked[files_key]:
                tracked[files_key].append(file)
        json.dump(tracked, b)
        b.close()
        pass
