from lit.command.BaseCommand import BaseCommand
import os
import sys
import json

class AddCommand(BaseCommand):
    def __init__(self, name, help_message):
        super().__init__(name, help_message)

    def run(self, *args):
        file_list = self.get_file_list(sys.argv[2:])
        print(file_list)
        if not file_list == None:
           a = open('.lit/tracked_files.json', 'r')
           tracked = json.load(a)
           a.close()
           self.save_tracked_files(file_list, tracked)
        else:
            pass

    def get_file_list(self, *args):
        file_list = []
        for root, dirs, files in os.walk(args[0][0]):
            for f in files:
                path = os.path.join(root, f)
                file_list.append(path)
        return file_list

    def save_tracked_files(self, file_list, tracked):

        b = open('.lit/tracked_files.json', 'w')
        for file in file_list:
            if file not in tracked['files']:
                tracked['files'].append(file)
        json.dump(tracked, b)
        b.close()
        pass





