from lit.command.BaseCommand import BaseCommand
import os


class InitCommand(BaseCommand):
    def __init__(self, name, help_message):
        super().__init__(name, help_message)

    def run(self, **args):
        if not os.path.exists('.lit'):
            os.makedirs('.lit')
            os.makedirs('.lit/commits')
            with open('.lit/tracked_files.json', 'w') as outfile:
                pass
            with open('.lit/commits_log.json', 'w') as outfile:
                outfile.write('[]')
        else:
            print('LIT has been already inited in this directory')
#        if not super().run():
#            return False
#        raise NotImplementedError()
