import os
import zipfile
import lit.paths
import shutil
from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.StringManager import StringManager
from lit.file.SettingsManager import SettingsManager
from lit.file.JSONSerializer import JSONSerializer
import lit.diff.roberteldersoftwarediff as diff
from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.strings_holder import DiffStrings


class DiffCommand(BaseCommand):
    __TEMP_PATH = '/tmp/lit'

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

    def run(self, **args):
        if not super().run():
            return False

        # get last commit short hash
        serializer = JSONSerializer(SettingsManager.get_var_value('COMMIT_LOG_PATH'))
        commits = serializer.read_all_items()['commits']
        last_commit = commits[len(commits) - 1]
        last_commit_short_hash = last_commit["short_hash"]

        # unzip last commit snapshot
        commits_dir_path = os.path.join(lit.paths.DIR_PATH, 'commits')
        zip_file_name = last_commit_short_hash + SettingsManager.get_var_value('COMMIT_ZIP_EXTENCION')
        zip_file_path = os.path.join(commits_dir_path, zip_file_name)
        zip_ref = zipfile.ZipFile(zip_file_path, 'r')
        try:
            os.mkdir(self.__TEMP_PATH)
        except FileExistsError:
            pass
        extracted_snapshot_path = os.path.join(self.__TEMP_PATH, last_commit_short_hash)
        try:
            os.mkdir(extracted_snapshot_path)
        except FileExistsError:
            pass
        zip_ref.extractall(extracted_snapshot_path)
        zip_ref.close()

        # run diff
        compared_file_name = args[DiffStrings.ARG_PATH_1_NAME.value]
        compared_file_path = os.path.join(os.getcwd(), compared_file_name)
        extracted_file_path = os.path.join(extracted_snapshot_path, compared_file_name)
        diff.main(
            [
                compared_file_path,
                extracted_file_path,
            ]
        )

        # remove extracted snapshot
        shutil.rmtree(extracted_snapshot_path)
