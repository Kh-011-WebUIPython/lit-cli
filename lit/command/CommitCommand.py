import hashlib
import json
import os
from datetime import datetime
from zipfile import *

from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.JSONSerializer import JSONSerializer
import hashlib
import lit.paths
import lit.util as util
from lit.strings_holder import CommitStrings, TrackedFileSettings, CommitSettings, \
    LogSettings, ProgramSettings, BranchSettings


class CommitCommand(BaseCommand):
    def __init__(self):
        name = CommitStrings.NAME
        help_message = CommitStrings.HELP
        arguments = [
            CommandArgument(
                name=CommitStrings.ARG_MSG_NAME,
                type=str,
                help=CommitStrings.ARG_MSG_HELP
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **kwargs):
        if not super().run():
            return False
        if not self.check_repo():
            return False

        # TODO REFACTOR!

        tracked_files_serializer = JSONSerializer(TrackedFileSettings.FILE_PATH)
        tracked_files_list = tracked_files_serializer.get_all_from_list_item(
            TrackedFileSettings.FILES_KEY)
        if not tracked_files_list:
            print('No files in staging area were found')
            return
        temp_zip_file_name = CommitSettings.TEMP_ZIP_FILE_PATH + CommitSettings.ZIP_EXTENSION
        temp_zip_file_path = os.path.join(CommitSettings.DIR_PATH, temp_zip_file_name)

        with ZipFile(temp_zip_file_path, 'w') as zip_file_ref:
            for file_name in tracked_files_list:
                zip_file_ref.write(file_name)

        zip_file_hash = util.get_file_hash(temp_zip_file_path)

        if zip_file_hash == util.get_last_commit_hash_in_branch(util.get_current_branch_name()):
            print('There is no changes since last commit')
            os.remove(temp_zip_file_path)
            return False

        ''' Change snapshot file name from temporary to permanent '''
        zip_file_name = str(zip_file_hash)[:CommitSettings.SHORT_HASH_LENGTH] + CommitSettings.ZIP_EXTENSION
        zip_file_path = os.path.join(CommitSettings.DIR_PATH, zip_file_name)
        os.rename(temp_zip_file_path, zip_file_path)

        commit_message = kwargs[CommitStrings.ARG_MSG_NAME]

        commit = {
            CommitSettings.USER: lit.util.get_user_name(),
            CommitSettings.LONG_HASH: zip_file_hash,
            CommitSettings.DATETIME: str(datetime.utcnow()),
            CommitSettings.MESSAGE: commit_message,
        }

        ''' Append commit to commits list in json file '''
        current_branch_log_file_path = util.get_current_branch_log_file_path()
        commits_log_serializer = JSONSerializer(current_branch_log_file_path)
        commits_log_serializer.append_to_list_item(LogSettings.COMMITS_LIST_KEY, commit)

        tracked_files_serializer.remove_all_from_list_item(TrackedFileSettings.FILES_KEY)
        return True
