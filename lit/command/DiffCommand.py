import lit.diff.roberteldersoftwarediff as diff
from lit.command.BaseCommand import BaseCommand, CommandArgument
from lit.strings_holder import StringsHolder


class DiffCommand(BaseCommand):
    def __init__(self):
        name = StringsHolder.Commands.Diff.NAME
        help_message = StringsHolder.Commands.Diff.HELP
        arguments = [
            CommandArgument(
                name=StringsHolder.Commands.Diff.Arguments.PATH_1_NAME,
                type=str,
                help=StringsHolder.Commands.Diff.Arguments.PATH_1_HELP
            ),
            CommandArgument(
                name=StringsHolder.Commands.Diff.Arguments.PATH_2_NAME,
                type=str,
                help=StringsHolder.Commands.Diff.Arguments.PATH_2_HELP
            ),
        ]
        super().__init__(name, help_message, arguments)

    def run(self, **args):
        if not super().run():
            return False
        diff.main(
            [
                args[StringsHolder.Commands.Diff.Arguments.PATH_1_NAME.value],
                args[StringsHolder.Commands.Diff.Arguments.PATH_2_NAME.value],
            ]
        )
