from lit.command.BaseCommand import BaseCommand
import json
import sys
import os
import glob


class RmCommand(BaseCommand):
    def __init__(self, name, help_message):
        super().__init__(name, help_message)

    def run(self, **args):
        delete_path = sys.argv[2:][0]

        (filepath, filename) = os.path.split(delete_path)
        (shortname, extension) = os.path.splitext(delete_path)

        print(filename)

        if extension == "":
            print("No extension")
            delete_list = os.listdir(delete_path)
            print(delete_list)

        else:
            print("i have extention" + extension)

            a = open('.lit/tracked_files.json', 'r')
            tracked = json.load(a)
            a.close()

            tracked['files'].remove(filename)

            b = open('.lit/tracked_files.json', 'w')
            json.dump(tracked, b)
            b.close()

 #

#        if not super().run():
#           return False
#        raise NotImplementedError()
