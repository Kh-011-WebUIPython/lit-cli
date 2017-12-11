from lit.command.BaseCommand import BaseCommand
from lit.file.StringManager import StringManager
from lit.file.SettingsManager import SettingsManager
import os


class InitCommand(BaseCommand):
    __COMMAND_INIT_NAME_KEY = 'COMMAND_INIT_NAME'
    __COMMAND_INIT_HELP_KEY = 'COMMAND_INIT_HELP'

    def __init__(self):
        name = StringManager.get_string(self.__COMMAND_INIT_NAME_KEY)
        help_message = StringManager.get_string(self.__COMMAND_INIT_HELP_KEY)
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
                pass
            with open(os.path.join(SettingsManager.get_var_value('INIT_LIT'),
                                   SettingsManager.get_var_value('INIT_COMMIT_LOG')), 'w') as outfile:
                outfile.write(SettingsManager.get_var_value('INIT_COMMIT_LOG_INIT'))
        else:
            print(SettingsManager.get_var_value('INIT_LIT_INITED'))
