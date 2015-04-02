####################################################################################################
# 
# Babel - A Bibliography Manager
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

import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime

####################################################################################################

from Babel.DataBase.SqlAlchemyBase import SqlRow

####################################################################################################

class FileRowMixin(SqlRow):

    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    added_time = Column(DateTime)
    
    path = Column(String, unique=True)
    inode = Column(Integer) # uniq on the same file-system
    # creation_time = Column(Integer)

    shasum = Column(String(64)) # allow for duplicates
    has_duplicate = Column(Boolean, default=False)

    title = Column(String, default='')
    author = Column(String, default='')
    comment = Column(String, default='')
    
    ##############################################
        
    def __repr__(self):
        
        message = '''
File Row
  path: {path}
  shasum: {shasum}
  inode: {inode}
  added time: {added_time}
  title: {title}
  author: {author}
  comment: {comment}
'''

        return message.format(self.get_column_dict())

    ##############################################

    def update(self, file_path):

        # Fixme: purpose
        
        if self.path != str(file_path):
            raise NameError("Attempt to update with a different path")
        self.shasum = file_path.shasum
        self.inode = file_path.inode
        # self.creation_time = file_path.creation_time
        
####################################################################################################

class FileTableMixin(object):

    ##############################################

    def add(self, file_path):

        file_row = self.ROW_CLASS(added_time=datetime.datetime.today(),
                                  path=str(file_path),
                                  inode=file_path.inode,
                                  shasum=file_path.shasum,
                                  # creation_time=file_path.creation_time,
                                 )
        self._session.add(file_row)

####################################################################################################
# 
# End
# 
####################################################################################################
