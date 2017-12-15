import os
import abc
from lit.strings_holder import ProgramSettings


class BaseCommand(abc.ABC):
    def __init__(self, name, help_message, arguments):
        self.__name = name
        self.__help_message = help_message
        if type(arguments) is not list:
            raise TypeError("'arguments' parameter must be a list of CommandArgument objects")
        for argument in arguments:
            if not isinstance(argument, CommandArgument):
                raise TypeError(
                    "'arguments' parameter must be a list of CommandArgument objects, not " + str(type(argument)))
        self.__arguments = arguments

    @abc.abstractmethod
    def run(self, **kwargs):
        """Abstract method for implementing command's logic.

        Arguments:
        **args -- optional arguments for command
        Returned value:
        True if command succeeded, else returns False
        """

        return True

    def run_argparse(self, argparse_args):
        """Converts arguments from argparse to suitable form"""
        kwargs = vars(argparse_args)
        self.run(**kwargs)

    @staticmethod
    def check_repo():
        if not os.path.exists(ProgramSettings.LIT_PATH):
            print('Error: current directory is not a lit repository')
            return False
        return True

    @property
    def name(self):
        return self.__name

    @property
    def help(self):
        return self.__help_message

    @property
    def arguments(self):
        return self.__arguments

    def __str__(self):
        return 'Command \'%s\': %s\n' % (self.name, self.help)


class CommandArgument():
    def __init__(self, name, type, help):
        self.__name = name
        self.__type = type
        self.__help = help

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type

    @property
    def help(self):
        return self.__help
