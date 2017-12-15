import os
from lit.command.BaseCommand import BaseCommand
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import LogSettings, LogStrings, CommitSettings


class LogCommand(BaseCommand):

    def __init__(self):
        name = LogStrings.NAME
        help_message = LogStrings.HELP
        arguments = []
        super().__init__(name, help_message, arguments)

    def run(self, **kwargs):
        if not super().run():
            return False
        if not self.check_repo():
            return False

        serializer = JSONSerializer(LogSettings.FILE_PATH)
        commits = serializer.get_all_from_list_item(LogSettings.COMMITS_LIST_KEY)
        self.print_commits_list(commits)

    @staticmethod
    def print_commits_list(commits):
        if len(commits) != 0:
            for commit in commits:
                short_hash = commit[CommitSettings.SHORT_HASH]
                message = commit[CommitSettings.COMMENT]
                user = commit[CommitSettings.USER]
                datetime = commit[CommitSettings.DATETIME]

                output = LogSettings.MESSAGE_FORMAT.format(short_hash, message, user, datetime)
                print(output)
        else:
            print(LogStrings.COMMITS_NOT_FOUND)
