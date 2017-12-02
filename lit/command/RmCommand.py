from lit.command.BaseCommand import BaseCommand
import json
import sys

class RmCommand(BaseCommand):
    def __init__(self, name, help_message):
        super().__init__(name, help_message)

    def run(self, **args):
        a = open('.lit/tracked_files.json', 'r')
        tracked = json.load(a)
        delete_file = sys.argv[2:]
        a.close()

        tracked["files"].pop(delete_file)

        b = open('.lit/tracked_files.json', 'w')
        json.dump(tracked, b)
        b.close()





#        if not super().run():
#           return False
#        raise NotImplementedError()
