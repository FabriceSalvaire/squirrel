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

####################################################################################################

import cmd

import colors # ansicolors @PyPI

from ..Config.ConfigFile import ConfigFile
from ..Logging import LogPrinting
from .Arguments import ShellArguments

####################################################################################################

class Shell(cmd.Cmd):

    intro = 'Manage Babel.   Type help or ? to list commands.\n'
    prompt = colors.green('Babel > ')

    # Cannot set attribute in __init__ ???
    _args = {}
    _application = None

    ##############################################

    def set_args(self, args):
        self._args = args

    ##############################################

    def _print_banner(self, title, width=100):

        print(
            colors.red(
                LogPrinting.format_message_header(
                    title,
                    width=width,
                    centered=True,
                    margin=True,
                    border=True,
                    bottom_rule=True,
                    newline=False,
                )
            )
        )

    ##############################################

    def _yes_no(self, message, default='y'):

        response = input(message + ' : y/n [{}]'.format(default)).lower().strip()
        if not response:
            response = default
        return response == 'y'

    ##############################################

    def _check_args(self, args, defaults=None):

        if isinstance(args, str):
            return ShellArguments(args, defaults)
        else:
            return args

    ##############################################

    @property
    def application(self):

        if self._application is None:
            from Babel.Application.BabelApplication import BabelApplication
            self._application = BabelApplication(args=self._args)
            self._application.execute_given_user_script()

        return self._application

    ##############################################

    def do_quit(self, arg=None):

        'Quit shell'

        return True

    ##############################################

    def do_show_version(self, arg=None):

        'Show version'

        import Babel.Version as Version
        print('Babel version is {}'.format(Version.babel))

    ##############################################

    def do_init(self, arg=None):

        'Make config file'

        # Fixme:
        args = self._check_args(arg, defaults=self._args)
        ConfigFile.create(args)

    ##############################################

    def do_index(self, arg=None):

        'Index'

        self.application.index_all(arg)

    ##############################################

    def do_search(self, arg=None):

        'Search'

        # Fixme:
        if isinstance(arg, str):
            args = ShellArguments('', defaults=dict(query=arg))
        else:
            args = arg
        self.application.console_search(args)

    ##############################################

    def do_corpus_search(self, arg=None):

        'Corpus Search'

        # Fixme:
        if isinstance(arg, str):
            args = ShellArguments('', defaults=dict(query=arg))
        else:
            args = arg
        self.application.console_corpus_search(args)

    ##############################################

    def do_database_statistics(self, arg=None):

        'Database statistics'

        self.application.console_database_statistics(arg)
