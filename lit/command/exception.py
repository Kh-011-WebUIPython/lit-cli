from lit.strings_holder import BranchSettings


class CommandError(Exception):
    pass


class CheckoutCommandError(CommandError):
    pass


class BranchNameNotFoundError(CheckoutCommandError):
    def __init__(self, log_file_path):
        self.__log_file_path = log_file_path

    def __str__(self):
        return 'JSON file {0} does not contain branch name key {1}' \
            .format(self.__log_file_path, BranchSettings.JSON_KEY_NAME)
