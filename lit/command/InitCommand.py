import os
from lit.command.BaseCommand import BaseCommand
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import ProgramSettings, CommitSettings, InitStrings, \
    TrackedFileSettings, LogSettings, BranchSettings, IgnoredFilesSettings


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

            settings_serializer = JSONSerializer(ProgramSettings.LIT_SETTINGS_PATH)
            settings_serializer.set_value(ProgramSettings.ACTIVE_BRANCH_KEY, ProgramSettings.ACTIVE_BRANCH_DEFAULT)
            settings_serializer.set_value(ProgramSettings.USER_NAME_KEY, ProgramSettings.USER_NAME_DEFAULT)

            tracked_files_serializer = JSONSerializer(TrackedFileSettings.FILE_PATH)
            tracked_files_serializer.create_list_item(TrackedFileSettings.FILES_KEY)

            default_branch_log_file_name = ProgramSettings.ACTIVE_BRANCH_DEFAULT + BranchSettings.JSON_FILE_NAME_SUFFIX
            default_branch_log_file_path = os.path.join(ProgramSettings.LIT_PATH, default_branch_log_file_name)
            commits_serializer = JSONSerializer(default_branch_log_file_path)
            commits_serializer.create_list_item(LogSettings.COMMITS_LIST_KEY)

            with open(IgnoredFilesSettings.FILE_PATH, 'w') as file:
                file.write(IgnoredFilesSettings.FILE_INITIAL_CONTENT)

            return True
        else:
            print(InitStrings.LIT_INITED)
            return False
