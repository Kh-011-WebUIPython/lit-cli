import os
from datetime import datetime
import zipfile
from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.JSONSerializer import JSONSerializer
import lit.util as util
from lit.strings_holder import CommitStrings, TrackedFileSettings, CommitSettings, LogSettings, SettingsStrings


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

        username = util.get_user_name()
        email = util.get_user_email()

        if not username or not email:
            print('Set up following settings first: ')
            if not username:
                print(" > {0}".format(SettingsStrings.ARG_NAME_CHOICE_USERNAME))
            if not email:
                print(" > {0}".format(SettingsStrings.ARG_NAME_CHOICE_EMAIL))
            return False

        current_branch_log_file_path = util.get_current_branch_log_file_path()
        commits_log_serializer = JSONSerializer(current_branch_log_file_path)

        tracked_files_serializer = JSONSerializer(TrackedFileSettings.FILE_PATH)
        tracked_files_set = tracked_files_serializer.get_all_from_set_item(
            TrackedFileSettings.FILES_KEY)

        unchanged_files, modified_files, new_files, deleted_files = self.get_files_status()

        if not tracked_files_set and not deleted_files:
            print('No files in staging area were found')
            return False

        if not modified_files and not new_files and not deleted_files:
            print('There are no changes since last commit')
            tracked_files_serializer.remove_all_from_list_item(TrackedFileSettings.FILES_KEY)
            return False

        temp_zip_file_name = CommitSettings.TEMP_FILE_PATH + CommitSettings.FILE_EXTENSION
        temp_zip_file_path = os.path.join(CommitSettings.DIR_PATH, temp_zip_file_name)

        last_commit_log = util.get_last_commit_log()

        # if file has not been changed since last commit
        # remove it from tracked files set
        # (a reference to prev commit will be added instead)
        if last_commit_log:
            last_commit_files = last_commit_log[CommitSettings.FILES_KEY]

            new_tracked_files_list = list(tracked_files_set)[:]
            for file_new in tracked_files_set:
                for file_old in last_commit_files:
                    if file_old[CommitSettings.FILES_PATH_KEY] == file_new:
                        file_new_hash = util.get_file_hash(file_new)
                        if file_old[CommitSettings.FILES_FILE_HASH_KEY] == file_new_hash:
                            new_tracked_files_list.remove(file_new)
                        break
            tracked_files_set = set(new_tracked_files_list)

        commit_message = kwargs[CommitStrings.ARG_MSG_NAME]

        commit_files_items_list = []

        zip_file_hash = "0"

        # if there are files to zip (changed/new files in staging area)
        if tracked_files_set:
            with zipfile.ZipFile(temp_zip_file_path, 'w') as zip_file_ref:
                for file_name in tracked_files_set:
                    zip_file_ref.write(file_name)

            zip_file_hash = util.get_file_hash(temp_zip_file_path)

            ''' Change snapshot file name from temporary to permanent '''
            zip_file_name = str(zip_file_hash)[:CommitSettings.SHORT_HASH_LENGTH] + CommitSettings.FILE_EXTENSION
            zip_file_path = os.path.join(CommitSettings.DIR_PATH, zip_file_name)
            os.rename(temp_zip_file_path, zip_file_path)

            for file_path in tracked_files_set:
                file_hash = util.get_file_hash(file_path)
                file_item = {
                    CommitSettings.FILES_PATH_KEY: file_path,
                    CommitSettings.FILES_FILE_HASH_KEY: file_hash,
                    CommitSettings.FILES_COMMIT_HASH_KEY: zip_file_hash,
                }
                commit_files_items_list.append(file_item)

        all_files_set = set(self.get_files_relative_path_list('.'))

        not_tracked_files = all_files_set.difference(tracked_files_set)

        if not_tracked_files:
            unchanged_files, modified_files, new_files, deleted_files = self.get_files_status(
                except_files=tracked_files_set)

            if unchanged_files or modified_files:

                if modified_files:
                    print('Warning: there are some files changed since last commit, but not added to staging area:')
                    for file in modified_files:
                        print(' * {0}'.format(file))

                # if file was in previous commit and is now present,
                # copy its info to new log entry
                if last_commit_log:
                    last_commit_files = last_commit_log[CommitSettings.FILES_KEY]
                    for file_path in not_tracked_files:
                        if file_path in unchanged_files or file_path in modified_files:
                            for file in last_commit_files:
                                if file[CommitSettings.FILES_PATH_KEY] == file_path:
                                    file_last_hash = file[CommitSettings.FILES_FILE_HASH_KEY]
                                    file_last_hash_commit = file[CommitSettings.FILES_COMMIT_HASH_KEY]
                                    break
                            else:
                                raise RuntimeError('File not found in last commit')

                            file_item = {
                                CommitSettings.FILES_PATH_KEY: file_path,
                                CommitSettings.FILES_FILE_HASH_KEY: file_last_hash,
                                CommitSettings.FILES_COMMIT_HASH_KEY: file_last_hash_commit,
                            }
                            commit_files_items_list.append(file_item)

        commit = {
            CommitSettings.USER_KEY: username,
            CommitSettings.EMAIL_KEY: email,
            CommitSettings.LONG_HASH_KEY: zip_file_hash,
            CommitSettings.DATETIME_KEY: str(datetime.utcnow()),
            CommitSettings.MESSAGE_KEY: commit_message,
            CommitSettings.FILES_KEY: list(commit_files_items_list),
        }

        ''' Append commit to commits list in json file '''
        commits_log_serializer.append_to_list_item(LogSettings.COMMITS_LIST_KEY, commit)

        tracked_files_serializer.remove_all_from_list_item(TrackedFileSettings.FILES_KEY)
        return True
