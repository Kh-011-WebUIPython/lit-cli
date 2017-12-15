import os
import importlib
from lit.command.BaseCommand import BaseCommand
from lit.strings_holder import ProgramSettings, CommitSettings, InitStrings, \
    TrackedFileSettings, LogSettings, InitSettings


class InitCommand(BaseCommand):
    def __init__(self):
        name = InitStrings.NAME
        help_message = InitStrings.HELP
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **kwargs):
        if not super().run():
            return False

        if not os.path.exists(ProgramSettings.LIT_PATH):
            os.mkdir(ProgramSettings.LIT_PATH)
            os.mkdir(os.path.join(ProgramSettings.LIT_PATH,
                                  CommitSettings.DIR_NAME))
            with open(os.path.join(ProgramSettings.LIT_PATH,
                                   TrackedFileSettings.FILE_NAME), 'w') as outfile:
                outfile.write(TrackedFileSettings.INIT_CONTENT)
            with open(os.path.join(ProgramSettings.LIT_PATH,
                                   LogSettings.FILE_NAME), 'w') as outfile:
                outfile.write(LogSettings.INIT_CONTENT)
            return True
        else:
            print(InitSettings.LIT_INITED)
            return False
