from lit.command.BaseCommand import BaseCommand
import json
from lit.strings_holder import StatusStrings


class StatusCommand(BaseCommand):
    def __init__(self):
        name = StatusStrings.NAME
        help_message = StatusStrings.HELP
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        if not super().run():
            return False
        with open(SettingsManager.get_var_value('TRACKED_FILE_PATH'), 'r') as file:
            json_data = json.load(file)
        print('Files in staging area:')
        print(*json_data['files'], sep='\n')
