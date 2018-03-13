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

# Fixme: convert to QML Model

####################################################################################################

from collections import OrderedDict

from Babel.FileSystem.File import Directory

####################################################################################################

class DirectoryToc:

    ##############################################

    def __init__(self, path):

        self._path = Directory(path)

        toc = {}
        for directory_path in self._path.iter_directories():
            directory = directory_path.basename()
            first_letter = directory[0].lower()
            if first_letter not in toc:
                toc[first_letter] = [directory_path]
            else:
                toc[first_letter].append(directory_path)
        for letter in toc:
            toc[letter].sort(key=lambda x: x.basename().lower())
        # letters = sorted(toc.keys())
        self._toc = OrderedDict(sorted(toc.items(), key=lambda t: t[0]))

    ##############################################

    @property
    def path(self):
        return self._path

    ##############################################

    @property
    def letters(self):
        return list(self._toc.keys())

    ##############################################

    def __getitem__(self, letter):
        return self._toc[letter]
