import os
from lit.command.BaseCommand import BaseCommand
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import ProgramSettings, CommitSettings, InitStrings, TrackedFileSettings, LogSettings


class InitCommand(BaseCommand):
    def __init__(self):
        name = InitStrings.NAME
        help_message = InitStrings.HELP
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **kwargs):
        if not super().run():
            return False

        if not os.path.exists(ProgramSettings.LIT_PATH):
            os.mkdir(ProgramSettings.LIT_PATH)
            os.mkdir(CommitSettings.DIR_PATH)

            tracked_files_serializer = JSONSerializer(TrackedFileSettings.FILE_PATH)
            tracked_files_serializer.create_list_item(TrackedFileSettings.FILES_KEY)

            commits_serializer = JSONSerializer(LogSettings.FILE_PATH)
            commits_serializer.create_list_item(LogSettings.COMMITS_LIST_KEY)

            return True
        else:
            print(InitStrings.LIT_INITED)
            return False
