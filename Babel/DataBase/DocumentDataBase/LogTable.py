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

__all__ = [
    'ImporterStatus',
    'ImporterLogRowMixin',
]

####################################################################################################

import enum

from sqlalchemy import Column, Integer, String, DateTime

from ..SqlAlchemyBase import SqlRow
from ..Types.Choice import ChoiceType

####################################################################################################

class ImporterStatus(enum.Enum):

    COMPLETED = 0
    TIMEOUT = 1
    CRASHED = 2

####################################################################################################

class ImporterLogRowMixin(SqlRow):

    __tablename__ = 'importer_log'

    id = Column(Integer, primary_key=True)
    path = Column(String)
    date = Column(DateTime)
    time = Column(Integer, nullable=True)
    status = Column(ChoiceType(ImporterStatus))

    ##############################################

    def __repr__(self):

        message = '''
Importer Log
  path: {0.path}
  date: {0.date}
  time: {0.time} s
  status: {0.status}
'''
        return message.format(self)
