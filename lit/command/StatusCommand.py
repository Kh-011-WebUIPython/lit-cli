from lit.command.BaseCommand import BaseCommand
from lit.strings_holder import StatusStrings, TrackedFileSettings, ProgramSettings
from lit.file.JSONSerializer import JSONSerializer


class StatusCommand(BaseCommand):
    def __init__(self):
        name = StatusStrings.NAME
        help_message = StatusStrings.HELP
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **kwargs):
        if not super().run():
            return False
        if not self.check_repo():
            return False

        self.print_current_branch()
        self.print_staging_area_content()
        return True

    @staticmethod
    def print_current_branch():
        settings_serializer = JSONSerializer(ProgramSettings.LIT_SETTINGS_PATH)
        current_branch = settings_serializer.get_value(ProgramSettings.ACTIVE_BRANCH_KEY)
        print('Current branch: {0}'.format(current_branch))

    @classmethod
    def print_staging_area_content(cls):
        tracked_files_serializer = JSONSerializer(TrackedFileSettings.FILE_PATH)
        files = set(tracked_files_serializer.get_value(TrackedFileSettings.FILES_KEY))

        if not files:
            print('Staging area is empty')
        else:
            print('Files in staging area:')
            for file in files:
                print(' > {0}'.format(file))

        unchanged_files, modified_files, new_files, deleted_files = cls.get_files_status(except_files=files)

        if modified_files:
            print('Modified files:')
            for file in modified_files:
                print(' * {0}'.format(file))

        if new_files:
            print('Untracked files:')
            for file in new_files:
                print(' + {0}'.format(file))

        if deleted_files:
            print('Deleted files:')
            for file in deleted_files:
                print(' - {0}'.format(file))
