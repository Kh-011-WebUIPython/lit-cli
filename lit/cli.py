import sys
import argparse
import lit.command.InitCommand as incom
import lit.command.AddCommand as addcom
import lit.command.CommitCommand as comcom
import lit.command.LogCommand as logcom


#sys.path.append("AddCommand", "BaseCommand", "CommitCommand", "DiffCommand",
#                "InitCommand", "LogCommand", "RmCommand", "StatusCommand")

#COMMANDS_INITIALIZE = {'add': sys.path.AddCommand('add', 'add files to tracked'),
#                       'commit': sys.path.CommitCommand('commit', 'commit tracked files'),
#                       'diff': sys.path.DiffCommand('diff', 'show difference of two files'),
#                       'init': sys.path.InitCommand('init', 'init lit directory'),
#                       'log': sys.path.LogCommand('log', 'show changes history'),
#                       'rm': sys.path.RmCommand('rm', 'delete selected file'),
#                       'status': sys.path.StatusCommand('status', 'show current status of changes'),
#                       }


init = incom.InitCommand('init', 'init lit directory')
add = addcom.AddCommand('add', 'add files to tracked')
commit = comcom.CommitCommand('commit','commit tracked files')
log = logcom.LogCommand('log', 'show changes history')


def main():
    parser = argparse.ArgumentParser(prog='lit', description='LIT version control system')
    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser('init', help='init help')
    #parser_init.set_defaults(func=COMMANDS_INITIALIZE['init'].run)
    parser_init.set_defaults(func=init.run)

    parser_add = subparsers.add_parser('add', help='add help')
    parser_add.add_argument('path', type=str, help='path help', action='store')
    parser_add.set_defaults(func=add.run)

    parser_rm = subparsers.add_parser('rm', help='rm help')
    parser_rm.add_argument('path', type=str, help='path help')
   # parser_rm.set_defaults(func=COMMANDS_INITIALIZE['rm'].run)

    parser_commit = subparsers.add_parser('commit', help='commit help')
    parser_commit.add_argument('message', type=str, help='message help')
    parser_commit.set_defaults(func = commit.run)
    #parser_commit.set_defaults(func=COMMANDS_INITIALIZE['commit'].run)

    parser_diff = subparsers.add_parser('diff', help='diff help')
    parser_diff.add_argument('file-1-path', type=str, help='file-1-path help')
    parser_diff.add_argument('file-2-path', type=str, help='file-2-path help')
    #parser_diff.set_default(func=COMMANDS_INITIALIZE['diff'].run)

    parser_log = subparsers.add_parser('log', help='log help')
    parser_log.set_defaults(func=log.run)
    #parser_log.add_defaults(func=COMMANDS_INITIALIZE['log'].run)

    parser_status = subparsers.add_parser('status', help='status help')
    #parser_status.add_defaults(func=COMMANDS_INITIALIZE['status'].run)

    result = parser.parse_args(sys.argv[1:])
    print(result)
    try:
        result.func()
    except:
        pass


if __name__ == '__main__':
    main()
