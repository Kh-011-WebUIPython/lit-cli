import json
import os

from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import AddStrings, TrackedFileSettings


class AddCommand(BaseCommand):

    def __init__(self):
        name = AddStrings.NAME
        help_message = AddStrings.HELP
        arguments = [
            CommandArgument(
                name=AddStrings.ARG_PATH_NAME,
                type=str,
                help=AddStrings.ARG_PATH_HELP
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        if not super().run():
            return False

        path = AddStrings.ARG_PATH_NAME
        file_list = self.get_file_list(args[path])
        if file_list == []:
            file_list = self.get_file(args[path])
        else:
            pass

        if not file_list == None:
            serializer = JSONSerializer(TrackedFileSettings.PATH)
            tracked = serializer.read_all_items()
            self.save_tracked_files(file_list, tracked)

    def get_file_list(self, *args):
        file_list = []
        for root, dirs, files in os.walk(args[0]):
            for f in files:
                path = os.path.join(root, f)
                if '.lit' not in path:
                    file_list.append(path)

        return file_list

    def get_file(self, *args):
        file_list = []
        path = os.path.join(args[0])
        file_list.append(path)
        return file_list

    def save_tracked_files(self, file_list, tracked):
        b = open(TrackedFileSettings.PATH, 'w')
        for file in file_list:
            files_key = TrackedFileSettings.FILES_KEY
            if file not in tracked[files_key]:
                tracked[files_key].append(file)
        json.dump(tracked, b)
        b.close()
        pass
