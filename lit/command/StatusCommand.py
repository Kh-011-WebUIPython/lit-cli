import json
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

    @staticmethod
    def print_current_branch():
        settings_serializer = JSONSerializer(ProgramSettings.LIT_SETTINGS_PATH)
        current_branch = settings_serializer.get_value(ProgramSettings.ACTIVE_BRANCH_KEY)
        print('Current branch: {0}'.format(current_branch))

    @staticmethod
    def print_staging_area_content():
        with open(TrackedFileSettings.FILE_PATH, 'r') as file:
            json_data = json.load(file)
        if len(json_data['files']) != 0:
            print('Files in staging area:')
            print(*json_data['files'], sep='\n')
        else:
            print('Staging area is empty')
