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
           print(tracked['files'][0])
           print(tracked['files'][0][0])
           print(tracked['files'][0][1])
           print(tracked['files'][0][2])



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

        for file in tracked['files']:
            for root, dirs, files in os.walk(sys.argv[2:]):
                for r in root:
                    if r not in file[0]:
                        contdir = []
                        for i in os.walk(r):
                            contdir.append(i)
                        file[0].append(contdir)
                for d in dirs:
                    if d not in file[1]:
                        contdir = []
                        for i in os.walk(d):
                            contdir.append(i)
                        file[1].append(contdir)
                for f in files:
                    if f not in file[2]:
                        contdir = []
                        for i in os.walk(f):
                            contdir.append(i)
                        file[2].append(contdir)

        json.dump(tracked, b)
        b.close()


def dupl(path, tracked):
    for file in tracked['files']:
        for root, dirs, files in os.walk(path):
            for r in root:
                if r not in file[0]:
                    contdir = []
                    for i in os.walk(r):
                        contdir.append(i)
                    file[0].append(contdir)
            for d in dirs:
                if d not in file[1]:
                    contdir = []
                    for i in os.walk(d):
                        contdir.append(i)
                    file[1].append(contdir)
            for f in files:
                if f not in file[2]:
                    contdir = []
                    for i in os.walk(f):
                        contdir.append(i)
                    file[2].append(contdir)

