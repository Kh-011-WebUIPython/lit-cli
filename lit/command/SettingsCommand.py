from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import ProgramSettings, SettingsStrings


class SettingsCommand(BaseCommand):
    def __init__(self):
        name = SettingsStrings.NAME
        help_message = SettingsStrings.HELP
        arguments = [
            CommandArgument(
                name=SettingsStrings.ARG_ACTION_NAME,
                type=str,
                help=SettingsStrings.ARG_ACTION_HELP,
                choices=(
                    SettingsStrings.ARG_ACTION_CHOICE_SET,
                    SettingsStrings.ARG_ACTION_CHOICE_GET,
                ),
            ),
            CommandArgument(
                name=SettingsStrings.ARG_NAME_NAME,
                type=str,
                help=SettingsStrings.ARG_NAME_HELP,
                choices=(
                    SettingsStrings.ARG_NAME_CHOICE_USERNAME,
                    SettingsStrings.ARG_NAME_CHOICE_EMAIL,
                ),
            ),
        ]

        super().__init__(name, help_message, arguments)

    def run(self, **kwargs):
        if not super().run():
            return False

        user_settings_serializer = JSONSerializer(ProgramSettings.LIT_USER_SETTINGS_PATH)

        action = kwargs[SettingsStrings.ARG_ACTION_NAME]
        setting_name = kwargs[SettingsStrings.ARG_NAME_NAME]

        if action == SettingsStrings.ARG_ACTION_CHOICE_SET:
            new_value = input('Enter new {0}: '.format(setting_name))
            while not len(new_value):
                new_value = input('Enter new {0}: '.format(setting_name))
            user_settings_serializer.set_value(setting_name, new_value)
            return True
        elif action == SettingsStrings.ARG_ACTION_CHOICE_GET:
            value = user_settings_serializer.get_value(setting_name)
            if value:
                print('{0}: {1}'.format(setting_name, value))
            else:
                print('{0} value is not set'.format(setting_name))
            return True
        else:
            return False
