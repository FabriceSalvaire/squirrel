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

class Arguments:

    ##############################################

    def __init__(self, **kwargs):

        self._args = kwargs

    ##############################################

    def __getattr__(self, key):
        return self._args.get(key, None)

    ##############################################

    def dump(self):

        for key, value in self._args.items():
            print('{} = {}'.format(key, value))

####################################################################################################

class ShellArguments(Arguments):

    ##############################################

    def __init__(self, args, defaults=None):

        # Fixme: '-' -> '_' ?

        super().__init__(defaults)

        for arg in args.split():
            if arg:
                if '=' in arg:
                    key, value = arg.split('=')
                    self._args[key] = value
                else:
                    self._args[arg] = True
