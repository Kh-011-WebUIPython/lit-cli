import abc


class BaseCommand(abc.ABC):
    def __init__(self, name, help_message):
        self.__name = name
        self.__help_message = help_message

    @abc.abstractmethod
    def run(self, **args):
        """Abstract method for implementing command's logic.

        Arguments:
        **args -- optional arguments for command
        Returned value:
        True if command succeeded, else returns False
        """
        pass

    @property
    def name(self):
        return self.__name

    @property
    def help(self):
        return self.__help_message

    def __str__(self):
        return 'Command \'%s\': %s\n' % (self.name, self.help)
