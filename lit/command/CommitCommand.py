from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.StringManager import StringManager


class CommitCommand(BaseCommand):
    __COMMAND_COMMIT_NAME_KEY = 'COMMAND_COMMIT_NAME'
    __COMMAND_COMMIT_HELP_KEY = 'COMMAND_COMMIT_HELP'
    __COMMAND_COMMIT_ARGUMENT_MESSAGE_NAME_KEY = 'COMMAND_COMMIT_ARGUMENT_MESSAGE_NAME'
    __COMMAND_COMMIT_ARGUMENT_MESSAGE_HELP_KEY = 'COMMAND_COMMIT_ARGUMENT_MESSAGE_HELP'

    def __init__(self):
        name = StringManager.get_string(self.__COMMAND_COMMIT_NAME_KEY)
        help_message = StringManager.get_string(self.__COMMAND_COMMIT_HELP_KEY)
        arguments = [
            CommandArgument(
                name=StringManager.get_string(self.__COMMAND_COMMIT_ARGUMENT_MESSAGE_NAME_KEY),
                type=str,
                help=StringManager.get_string(self.__COMMAND_COMMIT_ARGUMENT_MESSAGE_HELP_KEY)
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        if not super().run():
            return False
        raise NotImplementedError()
