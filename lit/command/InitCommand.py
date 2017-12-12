import os
from lit.command.BaseCommand import BaseCommand
from lit.strings_holder import CommitSettings, InitStrings, TrackedFileSettings, LogSettings, \
    InitSettings

class InitCommand(BaseCommand):
    def __init__(self):
        name = InitStrings.NAME
        help_message = InitStrings.HELP
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        if not os.path.exists(SettingsManager.get_var_value('INIT_LIT')):
            os.mkdir(SettingsManager.get_var_value('INIT_LIT'))
            os.mkdir(os.path.join(SettingsManager.get_var_value('INIT_LIT'),
                                  SettingsManager.get_var_value('INIT_COMMIT_DIR')))
            with open(os.path.join(SettingsManager.get_var_value('INIT_LIT'),
                                   SettingsManager.get_var_value('INIT_TRACKED_FILE')), 'w') as outfile:
                outfile.write(SettingsManager.get_var_value('INIT_TRACKED_FILE_INIT'))
        lit_dir = StringsHolder.InitSettings.LIT_DIR.value
        if not os.path.exists(lit_dir):
            os.makedirs(lit_dir)
            commit_dir = CommitSettings.DIR_NAME.value
            os.makedirs(os.path.join(lit_dir, commit_dir))
            tracked_file = TrackedFileSettings.FILE_NAME.value
            with open(os.path.join(lit_dir, tracked_file, 'w')) as outfile:
                outfile.write(TrackedFileSettings.INIT_CONTENT.value)
                pass
            log_file = LogSettings.FILE_NAME.value
            with open(os.path.join(lit_dir, log_file), 'w') as outfile:
                outfile.write(LogSettings.INIT_CONTENT.value)
        else:
            print(InitSettings.LIT_INITED)
