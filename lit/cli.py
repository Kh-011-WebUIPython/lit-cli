import sys
import argparse


def main():
    parser = argparse.ArgumentParser(prog='lit', description='LIT version control system')
    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser('init', help='init help')

    parser_add = subparsers.add_parser('add', help='add help')
    parser_add.add_argument('path', type=str, help='path help')

    parser_rm = subparsers.add_parser('rm', help='rm help')
    parser_rm.add_argument('path', type=str, help='path help')

    parser_commit = subparsers.add_parser('commit', help='commit help')
    parser_commit.add_argument('message', type=str, help='message help')

    parser_diff = subparsers.add_parser('diff', help='diff help')
    parser_diff.add_argument('file-1-path', type=str, help='file-1-path help')
    parser_diff.add_argument('file-2-path', type=str, help='file-2-path help')

    parser_log = subparsers.add_parser('log', help='log help')

    parser_status = subparsers.add_parser('status', help='status help')

    print(parser.parse_args(sys.argv[1:]))


if __name__ == '__main__':
    main()
