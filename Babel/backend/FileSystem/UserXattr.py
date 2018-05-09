####################################################################################################
#
# Babel - An Electronic Document Management System
# Copyright (C) 2017 Fabrice Salvaire
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

import xattr as Xattr

####################################################################################################

class UserXattr:

    ##############################################

    def __init__(self, path):

        self._xattr = Xattr.xattr(path)

    ##############################################

    @staticmethod
    def _user_xattr(name):

        return 'user.' + name

    ##############################################

    def __contains__(self, name):

        return self._user_xattr(name) in self._xattr

    ##############################################

    def keys(self, name):

        return [name for name in self._xattr.keys() if name.startwith('user:')]

    ##############################################

    def __setitem__(self, name, value):

        self._xattr[self._user_xattr(name)] = value.encode('ascii')

    ##############################################

    def __getitem__(self, name):

        return self._xattr[self._user_xattr(name)].decode('ascii')

    ##############################################

    def __delitem__(self, name):

        del self._xattr[self._user_xattr(name)]
