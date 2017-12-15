import os

from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import ProgramSettings, AddStrings, TrackedFileSettings


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

    def run(self, **kwargs):
        if not super().run():
            return False
        if not self.check_repo():
            return False

        path = kwargs[AddStrings.ARG_PATH_NAME]

        if os.path.exists(path):
            tracked_files_serializer = JSONSerializer(TrackedFileSettings.FILE_PATH)
            if os.path.isdir(path):
                tracked_files_serializer.add_set_to_set_item(
                    TrackedFileSettings.FILES_KEY,
                    self.get_files_relative_path_list(path)
                )
            else:
                tracked_files_serializer.add_to_set_item(TrackedFileSettings.FILES_KEY, path)
            return True
        else:
            return False

    @staticmethod
    def get_files_relative_path_list(starting_dir):
        file_relative_path_list = []
        for root, dirs, files in os.walk(starting_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_path = os.path.normpath(file_path)
                if ProgramSettings.LIT_DIR not in file_path:
                    file_relative_path_list.append(file_path)
        return file_relative_path_list
