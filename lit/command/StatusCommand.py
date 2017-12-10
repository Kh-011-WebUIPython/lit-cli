from lit.command.BaseCommand import BaseCommand
from lit.strings_holder import StringsHolder


class StatusCommand(BaseCommand):
    def __init__(self):
        name = StringsHolder.Commands.Status.NAME
        help_message = StringsHolder.Commands.Status.HELP
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        if not super().run():
            return False
        raise NotImplementedError()
