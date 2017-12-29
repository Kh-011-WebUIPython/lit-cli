import os
from lit.command.BaseCommand import BaseCommand, CommandArgument, FileStatus
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

    def run(self, **kwargs):
        if not super().run():
            return False
        if not self.check_repo():
            return False

        path = kwargs[AddStrings.ARG_PATH_NAME]

        if os.path.exists(path):
            tracked_files_serializer = JSONSerializer(TrackedFileSettings.FILE_PATH)
            if os.path.isdir(path):
                files_list = self.get_files_relative_path_list(path)
                unchanged_files, modified_files, new_files, deleted_files = self.get_files_status()
                files_list_to_add = set()
                for file in files_list:
                    if file in modified_files or file in new_files:
                        files_list_to_add.add(file)
                tracked_files_serializer.add_set_to_set_item(TrackedFileSettings.FILES_KEY, files_list_to_add)
            else:
                file_status = self.get_file_status(path)
                if file_status == FileStatus.MODIFIED or file_status == FileStatus.NEW:
                    tracked_files_serializer.add_to_set_item(TrackedFileSettings.FILES_KEY, path)
            return True
        else:
            return False


