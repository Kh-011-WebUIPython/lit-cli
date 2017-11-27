from lit.command.BaseCommand import BaseCommand


class LogCommand(BaseCommand):
    def __init__(self, name, help_message):
        super().__init__(name, help_message)

    def run(self, **args):
        if not super().run():
            return False
        raise NotImplementedError()
