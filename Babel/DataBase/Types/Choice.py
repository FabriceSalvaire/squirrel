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

from enum import Enum

from sqlalchemy import types

####################################################################################################

class ChoiceType(types.TypeDecorator):

    impl = types.Integer

    ##############################################

    def __init__(self, enum_class):

        super().__init__()

        if not issubclass(enum_class, Enum):
            raise ValueError('EnumType needs a class of enum defined.')

        self._enum_class = enum_class

    ##############################################

    def process_bind_param(self, value, dialect):

        if value is None:
            return None

        if isinstance(value, str):
            enum = getattr(self._enum_class, value)
        else:
            enum = self._enum_class(value)
        return enum.value

    ##############################################

    def process_result_value(self, value, dialect):

        if value is None:
            return None
        return self._enum_class(value)
