from lit.command.BaseCommand import BaseCommand
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import LogSettings, LogStrings, CommitSettings
import lit.util as util


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

        # TODO add optional detailed log (all info from JSON)

        current_branch_log_file_path = util.get_current_branch_log_file_path()

        serializer = JSONSerializer(current_branch_log_file_path)
        commits = serializer.get_all_from_list_item(LogSettings.COMMITS_LIST_KEY)
        self.print_commits_list(commits)

        return True

    @staticmethod
    def print_commits_list(commits):
        if len(commits) != 0:
            for commit in commits:
                short_hash = commit[CommitSettings.LONG_HASH_KEY][:CommitSettings.SHORT_HASH_LENGTH]
                message = commit[CommitSettings.MESSAGE_KEY]
                user = commit[CommitSettings.USER_KEY]
                email = commit[CommitSettings.EMAIL_KEY]
                datetime = commit[CommitSettings.DATETIME_KEY]

                output = LogSettings.MESSAGE_FORMAT.format(short_hash, user, email, message, datetime)
                print(output)
        else:
            print(LogStrings.COMMITS_NOT_FOUND)
