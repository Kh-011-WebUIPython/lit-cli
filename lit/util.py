import os
import shutil
import hashlib
import zipfile

from lit.file.JSONSerializer import JSONSerializer
import lit.paths
from lit.strings_holder import ProgramSettings, BranchSettings, CommitSettings, LogSettings


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


def unzip_commit_snapshot(commit_short_hash, extract_to):
    # TODO implement
    raise NotImplementedError


def unzip_commit(commit_short_hash, extract_to):
    if not os.path.exists(extract_to):
        raise FileNotFoundError('Dir \'' + extract_to + '\' not found')
    commits_dir_path = os.path.join(lit.paths.DIR_PATH, 'commits')
    zip_file_name = commit_short_hash + CommitSettings.FILE_EXTENSION
    zip_file_path = os.path.join(commits_dir_path, zip_file_name)
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
    settings_serializer = JSONSerializer(ProgramSettings.LIT_SETTINGS_PATH)
    user_name = settings_serializer.get_value(ProgramSettings.USER_NAME_KEY)
    return user_name


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
