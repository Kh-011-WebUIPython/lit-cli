from lit.command.BaseCommand import BaseCommand
import json
import sys
import os


class RmCommand(BaseCommand):
    def __init__(self, name, help_message):
        super().__init__(name, help_message)

    def run(self, **args):
        delete_path = sys.argv[2:][0]

        (filepath, filename) = os.path.split(delete_path)
        (shortname, extension) = os.path.splitext(delete_path)


        if extension == "":
            print("i have no extention")
            delete_list = os.listdir(delete_path)


            c = open('.lit/tracked_files.json', 'r')
            tracked = json.load(c)
            c.close()


            b = open('.lit/tracked_files.json', 'w')
            print(delete_path)
            print(delete_list)
            for file in tracked['files']:
                print(file)

                if file in delete_list:
                    print("i am in")
                    if not file.find(delete_path) == -1:
                        tracked['files'].remove(delete_path+'/'+file)
            json.dump(tracked, b)

            b.close()

        else:
            print("i have extention" + extension)

            a = open('.lit/tracked_files.json', 'r')
            tracked = json.load(a)
            a.close()

            tracked['files'].remove(delete_path)

            b = open('.lit/tracked_files.json', 'w')
            json.dump(tracked, b)
            b.close()
