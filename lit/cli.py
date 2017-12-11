#!/usr/bin/python3

import sys
import argparse
import lit.paths
import lit.init_settings
import lit.init_strings
from lit.file.JSONSerializer import JSONSerializer
from lit.file.StringManager import StringManager
from lit.file.SettingsManager import SettingsManager
from lit.command.AddCommand import AddCommand
from lit.command.CommitCommand import CommitCommand
from lit.command.DiffCommand import DiffCommand
from lit.command.InitCommand import InitCommand
from lit.command.LogCommand import LogCommand
from lit.command.RmCommand import RmCommand
from lit.command.StatusCommand import StatusCommand


def main_run(prog_name, desc, commands):
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


def main():
    strings_serializer = JSONSerializer(lit.paths.STRINGS_PATH)
    StringManager.init(strings_serializer)

    StringManager.set_strings(lit.init_strings.STRINGS)

    settings_serializer = JSONSerializer(lit.paths.SETTINGS_PATH)
    SettingsManager.init(settings_serializer)

    for k, v in lit.init_settings.SETTINGS.items():
        SettingsManager.set_var_value(k, v)

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

    main_run(program_name, description, commands)


if __name__ == '__main__':
    main()
