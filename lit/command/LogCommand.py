from lit.command.BaseCommand import BaseCommand
from lit.file.StringManager import StringManager


class LogCommand(BaseCommand):
    __COMMAND_LOG_NAME_KEY = 'COMMAND_LOG_NAME'
    __COMMAND_LOG_HELP_KEY = 'COMMAND_LOG_HELP'

    def __init__(self):
        name = StringManager.get_string(self.__COMMAND_LOG_NAME_KEY)
        help_message = StringManager.get_string(self.__COMMAND_LOG_HELP_KEY)
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        if not super().run():
            return False
        raise NotImplementedError()
