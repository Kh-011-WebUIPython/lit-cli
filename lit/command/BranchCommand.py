import os
import shutil
from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.file.JSONSerializer import JSONSerializer
from lit.strings_holder import ProgramSettings, BranchStrings, BranchSettings
import lit.util as util


class BranchCommand(BaseCommand):
    def __init__(self):
        name = BranchStrings.NAME
        help_message = BranchStrings.HELP
        arguments = [
            CommandArgument(
                name=BranchStrings.ARG_ACTION_NAME,
                type=str,
                help=BranchStrings.ARG_ACTION_HELP,
                choices=(
                    BranchStrings.ARG_ACTION_CHOICE_CREATE,
                    BranchStrings.ARG_ACTION_CHOICE_DELETE
                )
            ),
            CommandArgument(
                name=BranchStrings.ARG_NAME_NAME,
                type=str,
                help=BranchStrings.ARG_NAME_HELP,
            ),
        ]

        super().__init__(name, help_message, arguments)

    def run(self, **kwargs):
        if not super().run():
            return False
        if not self.check_repo():
            return False

        new_branch_name = kwargs[BranchStrings.ARG_NAME_NAME]
        action = kwargs[BranchStrings.ARG_ACTION_NAME]

        # TODO add branch list command

        # TODO add parent branch field

        settings_serializer = JSONSerializer(ProgramSettings.LIT_SETTINGS_PATH)
        active_branch_name = settings_serializer.get_value(ProgramSettings.ACTIVE_BRANCH_KEY)

        if action == BranchStrings.ARG_ACTION_CHOICE_CREATE:
            return self.create_branch(new_branch_name, active_branch_name)
        elif action == BranchStrings.ARG_ACTION_CHOICE_DELETE:
            if new_branch_name == active_branch_name:
                print('Cannot delete active branch \'{0}\''.format(active_branch_name))
                return False
            return self.delete_branch(new_branch_name)
        else:
            return False

    @classmethod
    def create_branch(cls, new_branch_name, active_branch_name):
        if cls.check_if_branch_exists(new_branch_name):
            print('Branch \'{0}\' already exists'.format(new_branch_name))
            return False

        old_branch_log_file_path = util.get_branch_log_file_path(active_branch_name)
        new_branch_log_file_path = util.get_branch_log_file_path(new_branch_name)

        shutil.copy(old_branch_log_file_path, new_branch_log_file_path)

        new_branch_serializer = JSONSerializer(new_branch_log_file_path)
        new_branch_serializer.set_value(BranchSettings.JSON_PARENT_BRANCH_NAME_KEY, active_branch_name)

        print('Branch \'{0}\' has been created successfully'.format(new_branch_name))
        return True

    @classmethod
    def delete_branch(cls, branch_name):
        if not cls.check_if_branch_exists(branch_name):
            print('Branch \'{0}\' does not exist'.format(branch_name))
            return False
        branch_log_file_path = util.get_branch_log_file_path(branch_name)
        os.remove(branch_log_file_path)
        print('Branch \'{0}\' has been removed successfully'.format(branch_name))
        return True
