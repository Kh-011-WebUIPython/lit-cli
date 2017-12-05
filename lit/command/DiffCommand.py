from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.StringManager import StringManager


class DiffCommand(BaseCommand):
    __COMMAND_DIFF_NAME_KEY = 'COMMAND_DIFF_NAME'
    __COMMAND_DIFF_HELP_KEY = 'COMMAND_DIFF_HELP'
    __COMMAND_DIFF_ARGUMENT_PATH_1_NAME_KEY = 'COMMAND_DIFF_ARGUMENT_PATH_1_NAME'
    __COMMAND_DIFF_ARGUMENT_PATH_1_HELP_KEY = 'COMMAND_DIFF_ARGUMENT_PATH_1_HELP'
    __COMMAND_DIFF_ARGUMENT_PATH_2_NAME_KEY = 'COMMAND_DIFF_ARGUMENT_PATH_2_NAME'
    __COMMAND_DIFF_ARGUMENT_PATH_2_HELP_KEY = 'COMMAND_DIFF_ARGUMENT_PATH_2_HELP'

    def __init__(self):
        name = StringManager.get_string(self.__COMMAND_DIFF_NAME_KEY)
        help_message = StringManager.get_string(self.__COMMAND_DIFF_HELP_KEY)
        arguments = [
            CommandArgument(
                name=StringManager.get_string(self.__COMMAND_DIFF_ARGUMENT_PATH_1_NAME_KEY),
                type=str,
                help=StringManager.get_string(self.__COMMAND_DIFF_ARGUMENT_PATH_1_HELP_KEY)
            ),
            CommandArgument(
                name=StringManager.get_string(self.__COMMAND_DIFF_ARGUMENT_PATH_2_NAME_KEY),
                type=str,
                help=StringManager.get_string(self.__COMMAND_DIFF_ARGUMENT_PATH_2_HELP_KEY)
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        if not super().run():
            return False
        raise NotImplementedError()
