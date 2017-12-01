from lit.command.BaseCommand import BaseCommand
import os
import sys
import json





class AddCommand(BaseCommand):

    path = os.getcwd()

    def __init__(self, name, help_message):
        super().__init__(name, help_message)

    def run(self, *args):
        print(self.get_file_list(sys.argv[2:]))
        file_list = self.get_file_list(sys.argv[2:])
        a = open('.lit/tracked_files.json', 'r')
        tracked = json.load( a )
        a.close()


        b = open('.lit/tracked_files.json', 'w')
        for file in file_list:
            if file not in (tracked.keys() or tracked.values()):
                json.dump(file,b )
        b.close()

 #       if args in self.get_file_list() and args not in self.tracked_files:
 #           self.tracked_files.append(args)
 #          self.save_tracked_files()


    def get_file_list(self, *args):
        print(args[0][0])
        file_list = os.listdir(args[0][0])
        return list(filter(lambda file: file[0] != '.', file_list))

    def save_tracked_files(self):
#       with open(self.path + '/.lit/tracked_files.json', 'w') as outfile:
#           json.dump(self.tracked_files, outfile)
        pass

#        if not super().run():
#           return False
#        raise NotImplementedError()
