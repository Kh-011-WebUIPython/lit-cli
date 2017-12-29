import os
from lit.command.BaseCommand import BaseCommand
from lit.command.BaseCommand import CommandArgument
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import RmStrings, TrackedFileSettings


class RmCommand(BaseCommand):
    def __init__(self):
        name = RmStrings.NAME
        help_message = RmStrings.HELP
        arguments = [
            CommandArgument(
                name=RmStrings.ARG_PATH_NAME,
                type=str,
                help=RmStrings.ARG_PATH_HELP
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **kwargs):
        if not super().run():
            return False
        if not self.check_repo():
            return False

        path = kwargs[RmStrings.ARG_PATH_NAME]

        if os.path.exists(path):
            tracked_files_serializer = JSONSerializer(TrackedFileSettings.FILE_PATH)
            if os.path.isdir(path):
                tracked_files_serializer.remove_set_from_set_item(
                    TrackedFileSettings.FILES_KEY,
                    self.get_files_relative_path_list(path)
                )
            else:
                tracked_files_serializer.remove_from_set_item(TrackedFileSettings.FILES_KEY, path)
            return True
        else:
            return False
