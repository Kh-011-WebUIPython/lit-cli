import os
import zipfile

from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import ProgramSettings, AddStrings, LogSettings, CheckoutStrings, \
    BranchSettings, CommitSettings, TrackedFileSettings
from lit.command.exception import BranchNameNotFoundError
import lit.util as util


class CheckoutCommand(BaseCommand):
    def __init__(self):
        name = CheckoutStrings.NAME
        help_message = CheckoutStrings.HELP
        arguments = [
            CommandArgument(
                name=CheckoutStrings.ARG_BRANCH_NAME,
                type=str,
                help=CheckoutStrings.ARG_BRANCH_HELP
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **kwargs):
        if not super().run():
            return False
        if not self.check_repo():
            return False

        branch_name = kwargs[CheckoutStrings.ARG_BRANCH_NAME]
        # TODO check branch_name for valid characters
        branches_names = self.get_all_branches_names()
        if branch_name in branches_names:
            print('Switching to branch {0}...'.format(branch_name), end='')
            self.restore_last_snapshot_for_branch(branch_name)
        else:
            ''' Create new *_commits_log.json for new branch '''
            print('Switching to NEW branch {0}...'.format(branch_name), end='')
            new_branch_log_file_name = branch_name + BranchSettings.JSON_FILE_NAME_SUFFIX
            new_branch_log_file_path = os.path.join(ProgramSettings.LIT_PATH, new_branch_log_file_name)
            new_branch_log_serializer = JSONSerializer(new_branch_log_file_path)
            new_branch_log_serializer.create_list_item(LogSettings.COMMITS_LIST_KEY)
            # TODO add checking modified files since last commit
            util.clear_dir_content(ProgramSettings.LIT_WORKING_DIRECTORY_PATH, except_dirs=ProgramSettings.LIT_DIR)
        ''' Set active branch in settings '''
        settings_serializer = JSONSerializer(ProgramSettings.LIT_SETTINGS_PATH)
        settings_serializer.set_value(ProgramSettings.ACTIVE_BRANCH_KEY, branch_name)
        ''' Clear staging area '''
        tracked_files_serializer = JSONSerializer(TrackedFileSettings.FILE_PATH)
        tracked_files_serializer.remove_all_from_list_item(TrackedFileSettings.FILES_KEY)

        print('done')

    @staticmethod
    def get_all_branches_names():
        branches_names = []
        lit_dir_content = os.listdir(ProgramSettings.LIT_PATH)
        for item in lit_dir_content:
            item_path = os.path.join(ProgramSettings.LIT_PATH, item)
            if os.path.isfile(item_path):
                if item.endswith(BranchSettings.JSON_FILE_NAME_SUFFIX):
                    branch_name = item[:-len(BranchSettings.JSON_FILE_NAME_SUFFIX)]
                    branches_names.append(branch_name)
        return branches_names

    @classmethod
    def restore_last_snapshot_for_branch(cls, branch_name):
        # TODO add checking modified files since last commit
        util.clear_dir_content(ProgramSettings.LIT_WORKING_DIRECTORY_PATH, except_dirs=ProgramSettings.LIT_DIR)
        last_commit_hash = util.get_last_commit_hash_in_branch(branch_name)
        ''' If last_commit_hash is not None, restore last commit content '''
        if last_commit_hash:
            util.unzip_commit_snapshot(last_commit_hash, ProgramSettings.LIT_WORKING_DIRECTORY_PATH)
