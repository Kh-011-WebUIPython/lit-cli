from lit.command.BaseCommand import BaseCommand
from lit.file.JSONSerializer import JSONSerializer

from lit.strings_holder import StringsHolder


class LogCommand(BaseCommand):
    def __init__(self):
        name = StringsHolder.Commands.Log.NAME
        help_message = StringsHolder.Commands.Log.HELP
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        serializer = JSONSerializer(StringsHolder.LogSettings.PATH)
        logs = serializer.read_all_items()
        json_commit_print(logs)


def json_commit_print(json):
    for commit in json[StringsHolder.LogSettings.KEY]:
        short_hash_ = commit[StringsHolder.CommitSettings.SHORT_HASH]
        comment = commit[StringsHolder.CommitSettings.COMMENT]
        user = commit[StringsHolder.CommitSettings.USER]
        datetime = commit[StringsHolder.CommitSettings.DATETIME]
        s = StringsHolder.LogSettings.COMMIT + short_hash_ + ";\n" + \
            StringsHolder.LogSettings.COMMIT_MESSAGE + comment + ";\n" + \
            StringsHolder.LogSettings.USERNAME + user + ";\n" + \
            StringsHolder.LogSettings.DATE + datetime[:19] + "\n"
        print(s)
