import os
import abc
import enum
import fnmatch

from lit.strings_holder import ProgramSettings, BranchSettings, LogSettings, CommitSettings, IgnoredFilesSettings
from lit.file.JSONSerializer import JSONSerializer
import lit.util as util


class BaseCommand(abc.ABC):
    def __init__(self, name, help_message, arguments):
        self.__name = name
        self.__help_message = help_message
        if type(arguments) is not list:
            raise TypeError("'arguments' parameter must be a list of CommandArgument objects")
        for argument in arguments:
            if not isinstance(argument, CommandArgument):
                raise TypeError(
                    "'arguments' parameter must be a list of CommandArgument objects, not " + str(type(argument)))
        self.__arguments = arguments

    @abc.abstractmethod
    def run(self, **kwargs):
        """Abstract method for implementing command's logic.

        Arguments:
        **args -- optional arguments for command
        Returned value:
        True if command succeeded, else returns False
        """

        return True

    def run_argparse(self, argparse_args):
        """Converts arguments from argparse to suitable form"""
        kwargs = vars(argparse_args)
        return self.run(**kwargs)

    @staticmethod
    def check_repo():
        if not os.path.exists(ProgramSettings.LIT_PATH):
            print('Error: current directory is not a lit repository')
            return False
        return True

    @staticmethod
    def get_files_relative_path_list(starting_dir):
        file_relative_path_list = []
        for root, dirs, files in os.walk(starting_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_path = os.path.normpath(file_path)
                if ProgramSettings.LIT_DIR not in file_path:
                    file_relative_path_list.append(file_path)
        return file_relative_path_list

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
    def get_file_status(cls, file_path):
        """ unchanged / modified / new """
        ignored_files = cls.get_ignored_files_paths()
        if file_path in ignored_files:
            return FileStatus.IGNORED
        current_branch_log_file_path = util.get_current_branch_log_file_path()
        commits_log_serializer = JSONSerializer(current_branch_log_file_path)
        commits = commits_log_serializer.get_all_from_list_item(LogSettings.COMMITS_LIST_KEY)
        if not commits:
            return FileStatus.NEW
        last_commit = commits[len(commits) - 1]
        files = last_commit[CommitSettings.FILES_KEY]
        for file in files:
            if file[CommitSettings.FILES_PATH_KEY] == file_path:
                if os.path.isfile(file_path):
                    file_hash = util.get_file_hash(file_path)
                    if file[CommitSettings.FILES_FILE_HASH_KEY] == file_hash:
                        return FileStatus.UNCHANGED
                    else:
                        return FileStatus.MODIFIED
                else:
                    return FileStatus.DELETED
        return FileStatus.NEW

    @classmethod
    def get_files_status(cls, except_files=None):
        if except_files is None:
            except_files = set()
        except_files.update(cls.get_ignored_files_paths())
        current_branch_log_file_path = util.get_current_branch_log_file_path()
        commits_log_serializer = JSONSerializer(current_branch_log_file_path)
        commits = commits_log_serializer.get_all_from_list_item(LogSettings.COMMITS_LIST_KEY)

        # if there were no commits yet, all files are new
        if not commits:
            new_files = set(cls.get_files_relative_path_list('.'))
            new_files.difference_update(except_files)
            return set(), set(), new_files, set()

        last_commit = commits[len(commits) - 1]
        files_from_last_commit = last_commit[CommitSettings.FILES_KEY]
        files_actual = cls.get_files_relative_path_list('.')
        deleted_files = set()
        for file in files_from_last_commit:
            file_path = file[CommitSettings.FILES_PATH_KEY]
            if file_path not in except_files:
                deleted_files.add(file_path)
        new_files = set()
        modified_files = set()
        unchanged_files = set()
        for file_new in files_actual:
            if file_new in except_files:
                continue
            for file_old in files_from_last_commit:
                if file_old[CommitSettings.FILES_PATH_KEY] == file_new:
                    file_actual_hash = util.get_file_hash(file_new)
                    if file_old[CommitSettings.FILES_FILE_HASH_KEY] == file_actual_hash:
                        unchanged_files.add(file_new)
                    else:
                        modified_files.add(file_new)
                    deleted_files.remove(file_new)
                    break
            else:
                new_files.add(file_new)
        return unchanged_files, modified_files, new_files, deleted_files

    @classmethod
    def get_ignored_files_paths(cls):
        try:
            with open(IgnoredFilesSettings.FILE_PATH) as ignored_files_file:
                lines = ignored_files_file.readlines()
        except (IOError, OSError):
            return set()
        ignored_files_paths_set = set()
        patterns = set()
        for line in lines:
            line = line.strip()
            """ 
            Remove comments from lines '#'
            Example 'test_*.doc #awesome pattern' --> 'test_*.doc'
            """
            if IgnoredFilesSettings.FILE_COMMENT_PREFIX in line:
                line = line[:line.index(IgnoredFilesSettings.FILE_COMMENT_PREFIX)].strip()
            if line:
                patterns.add(line)
        files = cls.get_files_relative_path_list('.')
        for pattern in patterns:
            for file in files:
                file_parts = util.split_path(file)
                if fnmatch.filter(file_parts, pattern):
                    ignored_files_paths_set.add(file)
        return ignored_files_paths_set

    @classmethod
    def check_if_branch_exists(cls, branch_name):
        return branch_name in cls.get_all_branches_names()

    @property
    def name(self):
        return self.__name

    @property
    def help(self):
        return self.__help_message

    @property
    def arguments(self):
        return self.__arguments

    def __str__(self):
        return 'Command \'%s\': %s\n' % (self.name, self.help)


class CommandArgument():
    def __init__(self, name, type, help, choices=None):
        self.__name = name
        self.__type = type
        self.__help = help
        self.__choices = choices

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type

    @property
    def help(self):
        return self.__help

    @property
    def choices(self):
        return self.__choices


class FileStatus(enum.Enum):
    UNCHANGED = 1
    MODIFIED = 2
    NEW = 3
    DELETED = 4
    IGNORED = 5
