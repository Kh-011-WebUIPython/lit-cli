from lit.command.BaseCommand import BaseCommand
from lit.file.JSONSerializer import JSONSerializer

from lit.strings_holder import LogSettings, LogStrings, CommitSettings

class LogCommand(BaseCommand):
    def __init__(self):
        name = LogStrings.NAME
        help_message = LogStrings.HELP
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        serializer = JSONSerializer(SettingsManager.get_var_value('COMMIT_LOG_PATH'))
        serializer = JSONSerializer(LogSettings.PATH)
        logs = serializer.read_all_items()
        json_commit_print(logs)


def json_commit_print(json):
    for commit in json["commits"]:
        s = SettingsManager.get_var_value('LOG_COMMIT') + commit["short_hash"] + ";\n" + \
            SettingsManager.get_var_value('LOG_COMMIT_MESSAGE') + commit["comment"] + ";\n" + \
            SettingsManager.get_var_value('LOG_USERNAME') + commit["user"] + ";\n" + \
            SettingsManager.get_var_value('LOG_DATE') + commit["datetime"][:19] + "\n"
    for commit in json[LogSettings.KEY]:
        short_hash_ = commit[CommitSettings.SHORT_HASH]
        comment = commit[CommitSettings.COMMENT]
        user = commit[CommitSettings.USER]
        datetime = commit[CommitSettings.DATETIME]
        s = LogSettings.COMMIT + short_hash_ + ";\n" + \
            LogSettings.COMMIT_MESSAGE + comment + ";\n" + \
            LogSettings.USERNAME + user + ";\n" + \
            LogSettings.DATE + datetime[:19] + "\n"
        print(s)
