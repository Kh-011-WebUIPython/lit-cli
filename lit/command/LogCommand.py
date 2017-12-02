from lit.command.BaseCommand import BaseCommand
import json

class LogCommand(BaseCommand):
    def __init__(self, name, help_message):
        super().__init__(name, help_message)

    def run(self, **args):
        b = open('.lit/commits_log.json', 'r')
        logs = json.load(b)
        json_commit_print(logs)
        b.close()




def json_commit_print(json):
    for commit in json["commits"]:
        s = "Commit: " + commit["short_hash"]+ ";\n" +\
            "Commit message: " + commit["comment"][0] + ";\n" + \
            "Username: " + commit["user"] + ";\n" + \
            "Date: " + commit["datetime"][:19] + "\n"
        print(s)
