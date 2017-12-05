from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.StringManager import StringManager


class AddCommand(BaseCommand):
    __COMMAND_ADD_NAME_KEY = 'COMMAND_ADD_NAME'
    __COMMAND_ADD_HELP_KEY = 'COMMAND_ADD_HELP'
    __COMMAND_ADD_ARGUMENT_PATH_NAME_KEY = 'COMMAND_ADD_ARGUMENT_PATH_NAME'
    __COMMAND_ADD_ARGUMENT_PATH_HELP_KEY = 'COMMAND_ADD_ARGUMENT_PATH_HELP'

    def __init__(self):
        name = StringManager.get_string(self.__COMMAND_ADD_NAME_KEY)
        help_message = StringManager.get_string(self.__COMMAND_ADD_HELP_KEY)
        arguments = [
            CommandArgument(
                name=StringManager.get_string(self.__COMMAND_ADD_ARGUMENT_PATH_NAME_KEY),
                type=str,
                help=StringManager.get_string(self.__COMMAND_ADD_ARGUMENT_PATH_HELP_KEY)
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        if not super().run():
            return False
        print('**args content: ' + str(args))
        path_key = StringManager.get_string(self.__COMMAND_ADD_ARGUMENT_PATH_NAME_KEY)
        print('path: ' + args[path_key])
        raise NotImplementedError()
