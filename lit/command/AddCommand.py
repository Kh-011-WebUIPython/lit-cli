from lit.command.BaseCommand import BaseCommand
import os
import sys
import json





class AddCommand(BaseCommand):

    path = os.getcwd()

    def __init__(self, name, help_message):
        super().__init__(name, help_message)

    def run(self, *args):

        file_list = self.get_file_list(sys.argv[2:])

        a = open('.lit/tracked_files.json', 'r')
        tracked = json.load( a )
        a.close()

        self.save_tracked_files(file_list, tracked)
#        b = open('.lit/tracked_files.json', 'w')
#        for file in file_list:
#            if file not in tracked:
#                tracked['files'].append(file)
#        json.dump(tracked, b)
#        b.close()

    def get_file_list(self, *args):
        print(args[0][0])
        file_list = os.listdir(args[0][0])
        return list(filter(lambda file: file[0] != '.', file_list))

    def save_tracked_files(self, file_list, tracked):
        b = open('.lit/tracked_files.json', 'w')
        for file in file_list:
            if file not in tracked['files']:
                tracked['files'].append(file)
        json.dump(tracked, b)
        b.close()

        pass

#        if not super().run():
#           return False
#        raise NotImplementedError()
