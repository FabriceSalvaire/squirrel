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

import sqlalchemy.types as types

from Babel.FileSystem.File import Directory, File

####################################################################################################

class DirectoryType(types.TypeDecorator):

    impl = types.String

    ##############################################

    def process_bind_param(self, value, dialect):
        return str(value)

    ##############################################

    def process_result_value(self, value, dialect):
        return Direcotry(value)

####################################################################################################

class FileType(types.TypeDecorator):

    impl = types.String

    ##############################################

    def process_bind_param(self, value, dialect):
        return str(value)

    ##############################################

    def process_result_value(self, value, dialect):
        return File(value)
