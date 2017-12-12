from lit.command.BaseCommand import BaseCommand
import json
from lit.strings_holder import StatusStrings, TrackedFileSettings


class StatusCommand(BaseCommand):
    def __init__(self):
        name = StatusStrings.NAME
        help_message = StatusStrings.HELP
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        if not super().run():
            return False

        with open(TrackedFileSettings.PATH, 'r') as file:
            json_data = json.load(file)
        if len(json_data['files']) != 0:
            print('Files in staging area:')
            print(*json_data['files'], sep='\n')
        else:
            print('Staging area is empty')
