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
                help=CheckoutStrings.ARG_BRANCH_HELP,
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

        settings_serializer = JSONSerializer(ProgramSettings.LIT_SETTINGS_PATH)
        active_branch_name = settings_serializer.get_value(ProgramSettings.ACTIVE_BRANCH_KEY)
        if branch_name == active_branch_name:
            print('Already on branch \'{0}\''.format(branch_name))
            return False

        if not self.check_if_branch_exists(branch_name):
            print('Branch \'{0}\' not found'.format(branch_name))
            return False

        # TODO add checking modified files since last commit
        # TODO WHERE TO GET LAST <FULL> SNAPSHOT???

        print('Switching to branch {0}...'.format(branch_name), end='')
        self.restore_last_snapshot_for_branch(branch_name)

        ''' Set active branch in settings '''
        settings_serializer.set_value(ProgramSettings.ACTIVE_BRANCH_KEY, branch_name)

        ''' Clear staging area '''
        tracked_files_serializer = JSONSerializer(TrackedFileSettings.FILE_PATH)
        tracked_files_serializer.remove_all_from_list_item(TrackedFileSettings.FILES_KEY)

        print('done')
        return True

    @classmethod
    def restore_last_snapshot_for_branch(cls, branch_name):
        util.clear_dir_content(ProgramSettings.LIT_WORKING_DIRECTORY_PATH, except_dirs=ProgramSettings.LIT_DIR)
        last_commit_hash = util.get_last_commit_hash_in_branch(branch_name)
        ''' If last_commit_hash is not None, restore last commit content '''
        if last_commit_hash:
            util.unzip_commit_snapshot(last_commit_hash, ProgramSettings.LIT_WORKING_DIRECTORY_PATH)

    @classmethod
    def get_current_repo_state_hash(cls):
        temp_zip_file_name = CommitSettings.TEMP_FILE_PATH + CommitSettings.FILE_EXTENSION
        temp_zip_file_path = os.path.join(CommitSettings.DIR_PATH, temp_zip_file_name)

        with zipfile.ZipFile(temp_zip_file_path, 'w') as zip_file_ref:
            for file_name in cls.get_files_relative_path_list('.'):
                zip_file_ref.write(file_name)

        zip_file_hash = util.get_file_hash(temp_zip_file_path)
        return zip_file_hash
