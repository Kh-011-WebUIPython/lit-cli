import os
import shutil
import hashlib
import zipfile
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import ProgramSettings, BranchSettings, CommitSettings, LogSettings, SettingsStrings


def clear_dir_content(dir_path, except_dirs=()):
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            if item not in except_dirs:
                shutil.rmtree(item_path)
        else:
            raise RuntimeError('Unknown type of object {0}'.format(item))


def unzip_file_from_commit(commit_hash, file_path, extract_to):
    commits_log_serializer = JSONSerializer(get_current_branch_log_file_path())
    commits = commits_log_serializer.get_all_from_list_item(LogSettings.COMMITS_LIST_KEY)

    # if commits list is not empty
    if commits:

        # find commit with necessary hash
        for commit in commits:
            if commit[CommitSettings.LONG_HASH_KEY] == commit_hash:
                commit_files = commit[CommitSettings.FILES_KEY]

                # find necessary file in commit
                for file in commit_files:
                    if file[CommitSettings.FILES_PATH_KEY] == file_path:
                        # get commit archive path
                        commit_short_hash_with_file = \
                            file[CommitSettings.FILES_COMMIT_HASH_KEY][:CommitSettings.SHORT_HASH_LENGTH]
                        commit_file_name = commit_short_hash_with_file + CommitSettings.FILE_EXTENSION
                        commit_file_path = os.path.join(CommitSettings.DIR_PATH, commit_file_name)

                        # unpack necessary file from archive
                        with zipfile.ZipFile(commit_file_path, 'r') as zip_ref:
                            zip_ref.extract(file[CommitSettings.FILES_PATH_KEY], path=extract_to)

                        # return unpacked file path
                        extracted_file_path = os.path.join(extract_to, file[CommitSettings.FILES_PATH_KEY])
                        return extracted_file_path
    return None


def unzip_commit(commit_short_hash, extract_to):
    if not os.path.exists(extract_to):
        raise FileNotFoundError('Dir \'' + extract_to + '\' not found')
    zip_file_name = commit_short_hash + CommitSettings.FILE_EXTENSION
    zip_file_path = os.path.join(CommitSettings.DIR_PATH, zip_file_name)
    zip_ref = zipfile.ZipFile(zip_file_path, 'r')
    zip_ref.extractall(extract_to)
    zip_ref.close()


def get_current_branch_name():
    settings_serializer = JSONSerializer(ProgramSettings.LIT_SETTINGS_PATH)
    current_branch_name = settings_serializer.get_value(ProgramSettings.ACTIVE_BRANCH_KEY)
    return current_branch_name


def get_branch_log_file_name(branch_name):
    return branch_name + BranchSettings.JSON_FILE_NAME_SUFFIX


def get_branch_log_file_path(branch_name):
    return os.path.join(ProgramSettings.LIT_PATH, get_branch_log_file_name(branch_name))


def get_current_branch_log_file_name():
    current_branch_name = get_current_branch_name()
    current_branch_log_file_name = current_branch_name + BranchSettings.JSON_FILE_NAME_SUFFIX
    return current_branch_log_file_name


def get_current_branch_log_file_path():
    current_branch_log_file_path = os.path.join(ProgramSettings.LIT_PATH, get_current_branch_log_file_name())
    return current_branch_log_file_path


def get_user_name():
    user_settings_serializer = JSONSerializer(ProgramSettings.LIT_USER_SETTINGS_PATH)
    user_name = user_settings_serializer.get_value(SettingsStrings.ARG_NAME_CHOICE_USERNAME)
    return user_name


def get_user_email():
    user_settings_serializer = JSONSerializer(ProgramSettings.LIT_USER_SETTINGS_PATH)
    user_email = user_settings_serializer.get_value(SettingsStrings.ARG_NAME_CHOICE_EMAIL)
    return user_email


def get_last_commit_hash_in_branch(branch_name):
    log_file_name = branch_name + BranchSettings.JSON_FILE_NAME_SUFFIX
    log_file_path = os.path.join(ProgramSettings.LIT_PATH, log_file_name)
    serializer = JSONSerializer(log_file_path)
    commits = serializer.get_all_from_list_item(LogSettings.COMMITS_LIST_KEY)
    ''' Check if branch have no commits '''
    if not commits:
        return None
    # TODO sort commits list by date
    last_commit = commits[len(commits) - 1]
    last_commit_hash = last_commit[CommitSettings.LONG_HASH_KEY]
    return last_commit_hash


def get_last_commit_hash():
    current_branch_name = get_current_branch_name()
    return get_last_commit_hash_in_branch(current_branch_name)


def get_last_commit_log():
    current_branch_log_file_path = get_current_branch_log_file_path()
    serializer = JSONSerializer(current_branch_log_file_path)
    commits = serializer.get_all_from_list_item(LogSettings.COMMITS_LIST_KEY)
    if not commits:
        return None
    last_commit = commits[len(commits) - 1]
    return last_commit


def get_file_hash(file_path):
    hsh = hashlib.sha256()
    with open(file_path, 'br') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hsh.update(chunk)
    return hsh.hexdigest()


def split_path(path):
    parts = []
    while True:
        head, tail = os.path.split(path)
        parts.append(tail)
        if not head or head == '/':
            break
        path = head
    return parts
