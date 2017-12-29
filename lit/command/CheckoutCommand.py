import os
import shutil
import zipfile
from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import ProgramSettings, LogSettings, CheckoutStrings, \
    CommitSettings, TrackedFileSettings, CheckoutSettings
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

        # if files were modified, abort checkout
        unchanged_files, modified_files, new_files, deleted_files = self.get_files_status()
        if modified_files or new_files or deleted_files:
            print('There are modified, new or deleted files since last commit, checkout canceled')
            return False

        # check if branch exists
        if not self.check_if_branch_exists(branch_name):
            print('Branch \'{0}\' not found'.format(branch_name))
            return False

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
        # TODO unpack all files (may be in different archives)
        # 1. unpack necessary commits to own folders in temp dir
        # 2. move necessary files from each unpacked commit to repo dir
        # 3. delete temp dir content

        commits_log_serializer = JSONSerializer(util.get_branch_log_file_path(branch_name))
        commits = commits_log_serializer.get_all_from_list_item(LogSettings.COMMITS_LIST_KEY)

        # if branch contains commits
        if commits:
            last_commit = commits[len(commits) - 1]
            last_commit_files = last_commit[CommitSettings.FILES_KEY]

            # collect set of necessary commits
            commits_hashes_to_unpack = set()
            for file in last_commit_files:
                file_commit_short_hash = file[CommitSettings.FILES_COMMIT_HASH_KEY]
                commits_hashes_to_unpack.add(file_commit_short_hash)

            # make temp dir for commits
            try:
                os.mkdir(CheckoutSettings.TEMP_DIR_PATH)
            except FileExistsError:
                pass

            # unpack all necessary commits to temp dir
            for commit_hash in commits_hashes_to_unpack:
                short_hash = commit_hash[:CommitSettings.SHORT_HASH_LENGTH]
                commit_dir_path = os.path.join(CheckoutSettings.TEMP_DIR_PATH, short_hash)
                try:
                    os.mkdir(commit_dir_path)
                except FileExistsError:
                    pass
                util.unzip_commit(short_hash, commit_dir_path)

            # move necessary files to repo dir
            for file in last_commit_files:
                file_path = file[CommitSettings.FILES_PATH_KEY]
                file_commit_short_hash = file[CommitSettings.FILES_COMMIT_HASH_KEY][:CommitSettings.SHORT_HASH_LENGTH]
                unpacked_commit_path = os.path.join(CheckoutSettings.TEMP_DIR_PATH, file_commit_short_hash)

                move_from = os.path.join(unpacked_commit_path, file_path)
                move_to = os.path.join(ProgramSettings.LIT_WORKING_DIRECTORY_PATH, file_path)

                dest_file_dir_path = os.path.dirname(move_to)
                try:
                    os.makedirs(dest_file_dir_path)
                except FileExistsError:
                    pass

                # print(('from: {0}' + os.linesep + 'to: {1}').format(move_from, move_to))
                shutil.move(move_from, move_to)

            # clear temp dir content
            # util.clear_dir_content(CheckoutSettings.TEMP_DIR_PATH)
            shutil.rmtree(CheckoutSettings.TEMP_DIR_PATH)

        # ''' If last_commit_hash is not None, restore last commit content '''
        # if last_commit_short_hash:
        #     util.unzip_commit_snapshot(last_commit_short_hash, ProgramSettings.LIT_WORKING_DIRECTORY_PATH)

    @classmethod
    def get_current_repo_state_hash(cls):
        temp_zip_file_name = CommitSettings.TEMP_FILE_PATH + CommitSettings.FILE_EXTENSION
        temp_zip_file_path = os.path.join(CommitSettings.DIR_PATH, temp_zip_file_name)

        with zipfile.ZipFile(temp_zip_file_path, 'w') as zip_file_ref:
            for file_name in cls.get_files_relative_path_list('.'):
                zip_file_ref.write(file_name)

        zip_file_hash = util.get_file_hash(temp_zip_file_path)
        return zip_file_hash
