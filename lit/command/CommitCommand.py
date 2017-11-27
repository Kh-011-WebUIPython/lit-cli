from lit.command.BaseCommand import BaseCommand


class CommitCommand(BaseCommand):
    def __init__(self, name, help_message):
        super().__init__(name, help_message)

    def run(self):
        super().run()
        # important stuff
