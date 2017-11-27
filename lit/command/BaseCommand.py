import abc


class BaseCommand(abc.ABC):
    def __init__(self, name, help_message):
        self.__name = name
        self.__help_message = help_message

    @abc.abstractmethod
    def run(self):
        pass

    @property
    def name(self):
        return self.__name

    @property
    def help(self):
        return self.__help_message

    def __str__(self):
        return 'Name: %s\nHelp: %s\n' % (self.name, self.help)
