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

class Entry:

    ##############################################

    def __init__(self, entry_type, identifier, pairs):

        self.entry_type = entry_type
        self.identifier = identifier
        self._fields = dict(pairs)

    ##############################################

    def __iter__(self):

        return iter(self._fields.keys())

    ##############################################

    def __getattr__(self, key):

        return self._fields[key]

    ##############################################

    __getitem__ = __getattr__

    ##############################################

    def __str__(self):

        text = "@%(entry_type)s{%(identifier)s,\n" % self.__dict__
        for key, value in self._fields.items():
            text += ' '*2 + key + ' = "' + value + '",\n'
        text += '}'

        return text
