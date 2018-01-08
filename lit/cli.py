#!/usr/bin/python3

import sys
import argparse
from lit.command.AddCommand import AddCommand
from lit.command.BranchCommand import BranchCommand
from lit.command.CheckoutCommand import CheckoutCommand
from lit.command.CommitCommand import CommitCommand
from lit.command.DiffCommand import DiffCommand
from lit.command.InitCommand import InitCommand
from lit.command.LogCommand import LogCommand
from lit.command.RmCommand import RmCommand
from lit.command.SettingsCommand import SettingsCommand
from lit.command.StatusCommand import StatusCommand
from lit.strings_holder import ProgramStrings, CommandStrings


def main_run(commands):
    parser = argparse.ArgumentParser(
        prog=ProgramStrings.NAME,
        description=ProgramStrings.DESCRIPTION)

    subparsers_action = parser.add_subparsers()
    subparsers = []
    for command in commands:
        subparser = subparsers_action.add_parser(command.name, help=command.help)
        subparser.set_defaults(function=command.run_argparse)
        for argument in command.arguments:
            subparser.add_argument(argument.name, type=argument.type, help=argument.help, choices=argument.choices)
        subparsers.append(subparser)

    if len(sys.argv) == 1:
        cli_args = ['--help']
    else:
        cli_args = sys.argv[1:]
    parsed = parser.parse_args(cli_args)
    if not parsed.function(parsed):
        print(CommandStrings.RUN_METHOD_ERROR_MESSAGE)


def main():
    commands = [
        AddCommand(),
        BranchCommand(),
        CheckoutCommand(),
        CommitCommand(),
        DiffCommand(),
        InitCommand(),
        LogCommand(),
        RmCommand(),
        SettingsCommand(),
        StatusCommand(),
    ]

    main_run(commands)


if __name__ == '__main__':
    main()
