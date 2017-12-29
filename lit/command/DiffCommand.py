import os
import shutil
import lit.diff.roberteldersoftwarediff as diff
from lit.file.JSONSerializer import JSONSerializer
from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.strings_holder import DiffStrings, LogSettings, CommitSettings, DiffSettings
import lit.util as util


class DiffCommand(BaseCommand):
    def __init__(self):
        name = DiffStrings.NAME
        help_message = DiffStrings.HELP
        arguments = [
            CommandArgument(
                name=DiffStrings.ARG_PATH_1_NAME,
                type=str,
                help=DiffStrings.ARG_PATH_1_HELP
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **kwargs):
        if not super().run():
            return False
        if not self.check_repo():
            return False

        # get last commit short hash
        log_file_serializer = JSONSerializer(util.get_current_branch_log_file_path())
        commits = log_file_serializer.get_all_from_list_item(LogSettings.COMMITS_LIST_KEY)

        if len(commits) == 0:
            print('No commits were found')
            return False

        last_commit = commits[len(commits) - 1]
        last_commit_hash = last_commit[CommitSettings.LONG_HASH_KEY]

        compared_file_name = kwargs[DiffStrings.ARG_PATH_1_NAME]
        compared_file_path = os.path.join(os.getcwd(), compared_file_name)

        # unzip last commit file
        extracted_file_path = self.unzip_file_from_commit_to_temp_dir(last_commit_hash, compared_file_name)

        if not extracted_file_path:
            print('Cannot find previous version of file {0}'.format(compared_file_name))
            return False

        # run diff
        diff.main(
            [
                extracted_file_path,
                compared_file_path,
            ]
        )

        # remove extracted snapshot
        shutil.rmtree(DiffSettings.TEMP_PATH)
        return True

    @staticmethod
    def unzip_file_from_commit_to_temp_dir(commit_hash, file_path):
        commit_short_hash = commit_hash[:CommitSettings.SHORT_HASH_LENGTH]
        extracted_snapshot_path = os.path.join(DiffSettings.TEMP_PATH, commit_short_hash)
        os.makedirs(extracted_snapshot_path, exist_ok=True)
        extracted_file_path = util.unzip_file_from_commit(commit_hash, file_path, extracted_snapshot_path)
        return extracted_file_path
