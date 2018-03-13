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

# Fixme: common part

####################################################################################################

import datetime
today = datetime.datetime.today

from sqlalchemy import Column, Integer, String, DateTime

####################################################################################################

from ..SqlAlchemyBase import SqlRow
from .Type import DirectoryType

####################################################################################################

class DocumentRootRowMixin(SqlRow):

    __tablename__ = 'document_roots'

    # Record ID
    id = Column(Integer, primary_key=True)
    record_creation_date = Column(DateTime)
    record_update_date = Column(DateTime)

    path = Column(DirectoryType, unique=True)

    ##############################################

    def __init__(self, path):

        self.record_creation_date = today()
        self.update_record_date()
        self.path = path

    ##############################################

    def update_record_date(self):
        self.record_update_date = today()

    ##############################################

    def __repr__(self):

        message = '''
Document Root Row
  ID:   {id}
  path: {path}
'''

        return message.format(self)
