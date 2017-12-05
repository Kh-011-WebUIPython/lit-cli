from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.StringManager import StringManager


class RmCommand(BaseCommand):
    __COMMAND_RM_NAME_KEY = 'COMMAND_RM_NAME'
    __COMMAND_RM_HELP_KEY = 'COMMAND_RM_HELP'
    __COMMAND_RM_ARGUMENT_PATH_NAME_KEY = 'COMMAND_RM_ARGUMENT_PATH_NAME'
    __COMMAND_RM_ARGUMENT_PATH_HELP_KEY = 'COMMAND_RM_ARGUMENT_PATH_HELP'

    def __init__(self):
        name = StringManager.get_string(self.__COMMAND_RM_NAME_KEY)
        help_message = StringManager.get_string(self.__COMMAND_RM_HELP_KEY)
        arguments = [
            CommandArgument(
                name=StringManager.get_string(self.__COMMAND_RM_ARGUMENT_PATH_NAME_KEY),
                type=str,
                help=StringManager.get_string(self.__COMMAND_RM_ARGUMENT_PATH_HELP_KEY)
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        if not super().run():
            return False
        raise NotImplementedError()
