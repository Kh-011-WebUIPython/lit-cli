from lit.command.BaseCommand import BaseCommand
from lit.strings_holder import StatusStrings


class StatusCommand(BaseCommand):
    def __init__(self):
        name = StatusStrings.NAME
        help_message = StatusStrings.HELP
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        if not super().run():
            return False
        raise NotImplementedError()
