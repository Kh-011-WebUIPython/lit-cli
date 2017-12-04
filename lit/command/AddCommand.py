from lit.command.BaseCommand import BaseCommand
import os
import sys
import json

class AddCommand(BaseCommand):
    def __init__(self, name, help_message):
        super().__init__(name, help_message)

    def run(self, *args):
        file_list = self.get_file_list(sys.argv[2:])

        if not file_list == None:
           a = open('.lit/tracked_files.json', 'r')
           tracked = json.load(a)
           a.close()
           self.save_tracked_files(file_list, tracked)
        else:
            pass

    def get_file_list(self, *args):
        pdir = args[0][0]
        contdir = []
        for i in os.walk(pdir):
            contdir.append(i)
        return  contdir

    def save_tracked_files(self, file_list, tracked):

        b = open('.lit/tracked_files.json', 'w')

        for file in file_list:
            if file not in tracked['files']:
                tracked['files'].append(file)
        json.dump(tracked, b)
        b.close()
        pass





