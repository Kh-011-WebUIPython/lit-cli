import os
import shutil
import re
from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import ProgramSettings, BranchStrings, BranchSettings, RemoteStrings
import lit.util as util


class RemoteCommand(BaseCommand):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def __init__(self):
        name = RemoteStrings.NAME
        help_message = RemoteStrings.HELP
        arguments = [
            CommandArgument(
                name=RemoteStrings.ARG_ACTION_NAME,
                type=str,
                help=RemoteStrings.ARG_ACTION_HELP,
                choices=(
                    RemoteStrings.ARG_ACTION_CHOICE_SET,
                    RemoteStrings.ARG_ACTION_CHOICE_GET
                )
            ),
            CommandArgument(
                name=RemoteStrings.ARG_NAME_NAME,
                type=str,
                help=RemoteStrings.ARG_NAME_HELP,
                choices=(
                    RemoteStrings.ARG_NAME_CHOICE_URL,
                    RemoteStrings.ARG_NAME_CHOICE_REPO_ID,
                )
            ),
        ]

        super().__init__(name, help_message, arguments)

    def run(self, **kwargs):
        if not super().run():
            return False
        if not self.check_repo():
            return False

        action = kwargs[RemoteStrings.ARG_ACTION_NAME]
        setting_name = kwargs[RemoteStrings.ARG_NAME_NAME]

        settings_serializer = JSONSerializer(ProgramSettings.LIT_SETTINGS_PATH)

        if action == RemoteStrings.ARG_ACTION_CHOICE_GET:
            value = settings_serializer.get_value(setting_name)
            if value:
                print('{0}: {1}'.format(setting_name, value))
            else:
                print('{0} value is not set'.format(setting_name))
            return True
        elif action == RemoteStrings.ARG_ACTION_CHOICE_SET:
            new_value = input('Enter new {0}: '.format(setting_name))
            while not len(new_value):
                new_value = input('Enter new {0}: '.format(setting_name))
            if setting_name == RemoteStrings.ARG_NAME_CHOICE_URL and not self.validate_url(new_value):
                print('{0} value is invalid'.format(RemoteStrings.ARG_NAME_CHOICE_URL))
                return False
            elif setting_name == RemoteStrings.ARG_NAME_CHOICE_REPO_ID and not self.validate_repo_id(new_value):
                print('{0} value is invalid'.format(RemoteStrings.ARG_NAME_CHOICE_REPO_ID))
                return False
            settings_serializer.set_value(setting_name, new_value)
            return True
        else:
            return False

    def validate_url(self, url):
        return self.regex.match(url) is not None

    @staticmethod
    def validate_repo_id(repo_id):
        try:
            int(repo_id)
        except ValueError:
            return False
        return True
