import json
import os

from lit.command.BaseCommand import BaseCommand
from lit.command.BaseCommand import CommandArgument
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import StringsHolder


class RmCommand(BaseCommand):
    def __init__(self):
        name = StringsHolder.Commands.Rm.NAME
        help_message = StringsHolder.Commands.Rm.HELP
        arguments = [
            CommandArgument(
                name=StringsHolder.Commands.Rm.Arguments.PATH_NAME,
                type=str,
                help=StringsHolder.Commands.Rm.Arguments.PATH_HELP
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **args):

        delete_path = args[StringsHolder.Commands.Rm.Arguments.PATH_NAME.value]

        (short_name, extension) = os.path.splitext(delete_path)

        tracked_file_path = StringsHolder.TrackedFileSettings.PATH.value
        serializer_tracked = JSONSerializer(tracked_file_path)
        tracked = serializer_tracked.read_all_items()

        if extension == "":
            delete_list = self.get_file_list(delete_path)

            for file in delete_list:
                if file in tracked[StringsHolder.TrackedFileSettings.FILES_KEY]:
                    tracked[StringsHolder.TrackedFileSettings.FILES_KEY].remove(file)

            b = open(tracked_file_path, 'w')
            json.dump(tracked, b)
            b.close()

        else:
            tracked['files'].remove(delete_path)

            b = open(tracked_file_path, 'w')
            json.dump(tracked, b)
            b.close()

    def get_file_list(self, *args):
        file_list = []
        for root, dirs, files in os.walk(args[0]):
            for f in files:
                path = os.path.join(root, f)
                file_list.append(path)
        return file_list
