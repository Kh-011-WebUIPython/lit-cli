import os
from lit.command.BaseCommand import BaseCommand
from lit.strings_holder import CommitSettings, InitStrings, TrackedFileSettings, LogSettings, InitSettings


class InitCommand(BaseCommand):
    def __init__(self):
        name = InitStrings.NAME
        help_message = InitStrings.HELP
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        if not os.path.exists(InitSettings.LIT_DIR):
            os.mkdir(InitSettings.LIT_DIR)
            os.mkdir(os.path.join(InitSettings.LIT_DIR,
                                  CommitSettings.DIR_NAME))
            with open(os.path.join(InitSettings.LIT_DIR,
                                   TrackedFileSettings.FILE_NAME), 'w') as outfile:
                outfile.write(TrackedFileSettings.INIT_CONTENT)
            with open(os.path.join(InitSettings.LIT_DIR,
                                   LogSettings.FILE_NAME), 'w') as outfile:
                outfile.write(LogSettings.INIT_CONTENT)
        else:
            print(InitSettings.LIT_INITED)
