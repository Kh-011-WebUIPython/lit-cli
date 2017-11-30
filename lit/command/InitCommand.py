from lit.command.BaseCommand import BaseCommand
import os


class InitCommand(BaseCommand):

    LIT = '.lit'
    LIT_INITED = 'LIT has been already inited in this directory'
    COMMIT_DIR = '/commits'
    TRACKED_FILE = '/tracked_files.json'
    COMMIT_LOG = '/commits_log.json'

    def __init__(self, name, help_message):
        super().__init__(name, help_message)

    def run(self, **args):
        if not os.path.exists(self.LIT):
            os.makedirs(self.LIT)
            os.makedirs(self.LIT + self.COMMIT_DIR)
            with open(self.LIT + self.TRACKED_FILE, 'w') as outfile:
                pass
            with open(self.LIT + self.COMMIT_LOG, 'w') as outfile:
                outfile.write('[]')
        else:
            print(self.LIT_INITED)
#        if not super().run():
#            return False
#        raise NotImplementedError()
