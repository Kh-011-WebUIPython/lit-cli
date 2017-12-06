#!/usr/bin/python3

import sys
import argparse
import lit.paths
from lit.file.JSONSerializer import JSONSerializer
from lit.file.StringManager import StringManager
from lit.command.AddCommand import AddCommand
from lit.command.CommitCommand import CommitCommand
from lit.command.DiffCommand import DiffCommand
from lit.command.InitCommand import InitCommand
from lit.command.LogCommand import LogCommand
from lit.command.RmCommand import RmCommand
from lit.command.StatusCommand import StatusCommand


def main(prog_name, desc, commands):
    parser = argparse.ArgumentParser(prog=prog_name, description=desc)
    subparsers_action = parser.add_subparsers()

    subparsers = []
    for command in commands:
        subparser = subparsers_action.add_parser(command.name, help=command.help)
        subparser.set_defaults(function=command.run_argparse)
        for argument in command.arguments:
            subparser.add_argument(argument.name, type=argument.type, help=argument.help)
        subparsers.append(subparser)

    if len(sys.argv) == 1:
        cli_args = ['--help']
    else:
        cli_args = sys.argv[1:]
    parsed = parser.parse_args(cli_args)
    parsed.function(parsed)


if __name__ == '__main__':
    strings_serializer = JSONSerializer(lit.paths.STRINGS_PATH)
    StringManager.init(strings_serializer)

    program_name = StringManager.get_string('PROGRAM_NAME')
    description = StringManager.get_string('PROGRAM_DESCRIPTION')

    commands = [
        AddCommand(),
        CommitCommand(),
        DiffCommand(),
        InitCommand(),
        LogCommand(),
        RmCommand(),
        StatusCommand(),
    ]

    main(program_name, description, commands)
