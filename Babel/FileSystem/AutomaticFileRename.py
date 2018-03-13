####################################################################################################
#
# Babel - An Electronic Document Management System
# Copyright (C) 2014 Fabrice Salvaire
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

import re

####################################################################################################

from .File import File

####################################################################################################

class AutomaticFileRename:

    """ This class implements a suffix generator to rename automatically duplicated file name.

    Example of usage::

      AutomaticFileRename('foo.py').generate()

    """

    ##############################################

    def __init__(self, file_path):

        """ The parameter *file_name* is the file name. """

        file_path = File(file_path)
        self._path = file_path.directory
        self._file_name, self._extension = file_path.split_extension()

    ##############################################

    def _last_cycle(self):

        """ Return the last cycle. """

        pattern = self._file_name + '-(\\d+)' + self._extension
        compiled_pattern = re.compile(pattern)

        cycle = 0
        for entry, match in self._path.filter_entries(compiled_pattern):
            current_cycle = int(match.groups()[0])
            cycle = max(current_cycle, cycle)

        return cycle

    ##############################################

    def _new_cycle(self):

        """ Return the next cycle. """

        return self._last_cycle() +1

    ##############################################

    def generate(self):

        """ Return the backup file name. """

        file_name = self._file_name + '-' + str(self._new_cycle()) + self._extension
        return self._path.join_filename(file_name)
