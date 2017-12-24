import os
import shutil
import zipfile
import lit.paths
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
        last_commit_short_hash = last_commit[CommitSettings.LONG_HASH_KEY][:CommitSettings.SHORT_HASH_LENGTH]

        # unzip last commit snapshot
        extracted_snapshot_path = self.unzip_commit_snapshot_to_temp_dir(last_commit_short_hash)

        # run diff
        compared_file_name = kwargs[DiffStrings.ARG_PATH_1_NAME]
        compared_file_path = os.path.join(os.getcwd(), compared_file_name)
        extracted_file_path = os.path.join(extracted_snapshot_path, compared_file_name)
        diff.main(
            [
                extracted_file_path,
                compared_file_path,
            ]
        )

        # remove extracted snapshot
        shutil.rmtree(extracted_snapshot_path)
        return True

    @staticmethod
    def unzip_commit_snapshot_to_temp_dir(commit_hash):
        try:
            os.mkdir(DiffSettings.TEMP_PATH)
        except FileExistsError:
            pass
        extracted_snapshot_path = os.path.join(DiffSettings.TEMP_PATH, commit_hash)
        try:
            os.mkdir(extracted_snapshot_path)
        except FileExistsError:
            pass
        util.unzip_commit_snapshot(commit_hash, extracted_snapshot_path)
        return extracted_snapshot_path
