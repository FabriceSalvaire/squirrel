####################################################################################################
#
# Babel - An Electronic Document Management System
# Copyright (C) 2018 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

__all__ = [
    'ArgumentParser',
]

####################################################################################################

import argparse

from Babel.Tools.ProgramOptions import PathAction

####################################################################################################

class ArgumentParser:

    ##############################################

    def __init__(self, shell):

        self._shell = shell

        self._parser = argparse.ArgumentParser(
            description='Babel is an Electronic Document Management System',
        )

        subparsers = self._parser.add_subparsers(
            dest='subparser_name',
            title='subcommands',
            description='valid subcommands',
            # help='additional help',
            help='sub-command help',
        )

        ################################

        self._parser.add_argument(
            '--config',
            action=PathAction,
            default=None,
            help='config file',
        )

        self._parser.add_argument(
            '--version',
            action='store_true', default=False,
            help="show version and exit",
        )

        self._parser.add_argument(
            '--user-script',
            action=PathAction,
            default=None,
            help='user script to execute',
        )

        self._parser.add_argument(
            '--user-script-args',
            default='',
            help="user script args (don't forget to quote)",
        )

        ################################

        shell_parser = subparsers.add_parser(
            'shell',
            help='Run shell',
        )

        # shell_parser.set_defaults(func=shell.cmdloop)

        ################################

        init_parser = subparsers.add_parser(
            'init',
            help='Generate a config file',
        )

        init_parser.add_argument(
            '--document-root-path',
            action=PathAction,
            required=True,
            help='directory where are stored the documents',
        )

        init_parser.set_defaults(func=shell.do_init)

        ################################

        index_parser = subparsers.add_parser(
            'index',
            help='Index'
        )
        index_parser.set_defaults(func=shell.do_index)

        ################################

        search = subparsers.add_parser(
            'search',
            help='Search in the document database',
        )

        search.add_argument(
            'query', metavar='Query',
            help='Query',
        )

        search.set_defaults(func=shell.do_search)

        ################################

        corpus_search = subparsers.add_parser(
            'corpus_search',
            help='Search in the corpus database',
        )

        corpus_search.add_argument(
            'query', metavar='Query',
            help='Query',
        )

        corpus_search.set_defaults(func=shell.do_corpus_search)

        ################################

        database_statistics = subparsers.add_parser(
            'database_statistics',
            help='Show database statistics',
        )

        # database_statistics.add_argument(
        # )

        database_statistics.set_defaults(func=shell.do_database_statistics)

    ##############################################

    def parse(self):

        args = self._parser.parse_args()
        self._shell.set_args(args)

        # Call command
        if args.subparser_name == 'shell':
            self._shell.cmdloop()
        elif 'func' in args:
            args.func(args)
        else:
            self._parser.print_help()
