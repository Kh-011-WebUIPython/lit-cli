import lit.diff.roberteldersoftwarediff as diff
from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.strings_holder import DiffStrings


class DiffCommand(BaseCommand):
    def __init__(self):
        name = DiffStrings.NAME
        help_message = DiffStrings.HELP
        arguments = [
            CommandArgument(
                name=DiffStrings.ARG_PATH_1_NAME,
                type=str,
                help=DiffStrings.ARG_PATH_1_HELP
            ),
            CommandArgument(
                name=DiffStrings.ARG_PATH_2_NAME,
                type=str,
                help=DiffStrings.ARG_PATH_2_HELP
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        if not super().run():
            return False
        diff.main(
            [
                args[DiffStrings.ARG_PATH_1_NAME.value],
                args[DiffStrings.ARG_PATH_2_NAME.value],
            ]
        )
