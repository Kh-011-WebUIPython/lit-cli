from lit.command.BaseCommand import BaseCommand
from lit.file.StringManager import StringManager
import os


class InitCommand(BaseCommand):
    __COMMAND_INIT_NAME_KEY = 'COMMAND_INIT_NAME'
    __COMMAND_INIT_HELP_KEY = 'COMMAND_INIT_HELP'

    def __init__(self):
        name = StringManager.get_string(self.__COMMAND_INIT_NAME_KEY)
        help_message = StringManager.get_string(self.__COMMAND_INIT_HELP_KEY)
        arguments = []
        super().__init__(name, help_message, arguments)
    LIT = '.lit'
    LIT_INITED = 'LIT has been already inited in this directory'
    COMMIT_DIR = '/commits'
    TRACKED_FILE = '/tracked_files.json'
    COMMIT_LOG = '/commits_log.json'
    TRACKED_FILE_INIT = '{"files": []}'
    COMMIT_LOG_INIT = '{"commits":[]}'

    def run(self, **args):
        if not os.path.exists(self.LIT):
            os.makedirs(self.LIT)
            os.makedirs(self.LIT + self.COMMIT_DIR)
            with open(self.LIT + self.TRACKED_FILE, 'w') as outfile:
                outfile.write(self.TRACKED_FILE_INIT)
                pass
            with open(self.LIT + self.COMMIT_LOG, 'w') as outfile:
                outfile.write(self.COMMIT_LOG_INIT)
        else:
            print(self.LIT_INITED)
