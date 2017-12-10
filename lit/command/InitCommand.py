import os

from lit.command.BaseCommand import BaseCommand
from lit.strings_holder import StringsHolder


class InitCommand(BaseCommand):
    def __init__(self):
        name = StringsHolder.Commands.Init.NAME
        help_message = StringsHolder.Commands.Init.HELP
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        lit_dir = StringsHolder.InitSettings.LIT_DIR.value
        if not os.path.exists(lit_dir):
            os.makedirs(lit_dir)
            commit_dir = StringsHolder.CommitSettings.DIR_NAME.value
            os.makedirs(os.path.join(lit_dir, commit_dir))
            tracked_file = StringsHolder.TrackedFileSettings.FILE_NAME.value
            with open(os.path.join(lit_dir, tracked_file, 'w')) as outfile:
                outfile.write(StringsHolder.TrackedFileSettings.INIT_CONTENT.value)
                pass
            log_file = StringsHolder.LogSettings.FILE_NAME.value
            with open(os.path.join(lit_dir, log_file), 'w') as outfile:
                outfile.write(StringsHolder.LogSettings.INIT_CONTENT.value)
        else:
            print(StringsHolder.InitSettings.LIT_INITED)
