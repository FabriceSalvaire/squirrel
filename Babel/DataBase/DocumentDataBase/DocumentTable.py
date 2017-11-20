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
today = datetime.datetime.today

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
import sqlalchemy.types as types

####################################################################################################

from Babel.DataBase.SqlAlchemyBase import SqlRow
from Babel.FileSystem.File import File

####################################################################################################

class FileType(types.TypeDecorator):

    impl = types.String

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        return File(value)

####################################################################################################

class DocumentRowMixin(SqlRow):

    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    record_creation_date = Column(DateTime)
    record_update_date = Column(DateTime)

    path = Column(FileType, unique=True)
    inode = Column(Integer) # uniq on the same file-system
    # creation_time = Column(Integer)

    shasum = Column(String(64)) # duplicates are allowed
    has_duplicate = Column(Boolean, default=False)

    indexation_date = Column(DateTime, default=None) # to compare with indexer generation
    indexed_until = Column(Integer, default=0) # should be equal to number_of_pages
                                               # page number start from 1, 0 means not indexed
    indexation_status = Column(String, default='') # Fixme:
    language = Column(String(10), default='') # Fixme: en
    # indexer settings

    number_of_pages = Column(Integer)
    title = Column(String, default='')
    author = Column(String, default='')
    comment = Column(String, default='')

    ##############################################

    def __init__(self, file_path):

        self.record_creation_date = today()
        self.update_record_date()
        self.path = file_path
        self.inode = file_path.inode
        self.shasum = file_path.compute_shasum() # Fixme: .shasum

    ##############################################

    def update_record_date(self):
        self.record_update_date = today()

    ##############################################

    def update_indexation_date(self):
        self.indexation_date = today()

    ###############################################

    @declared_attr
    def words(self):
        return relationship('WordRow', order_by='WordRow.count', backref='document',
                            cascade="all, delete, delete-orphan",
                            )

    ##############################################

    def __repr__(self):

        message = '''
Document Row
  path: {path}
  shasum: {shasum}
  inode: {inode}
  record date: {record_creation_date}
  update date: {record_update_date}
  number of pages: {number_of_pages}
  title: {title}
  author: {author}
  comment: {comment}
'''

        return message.format(**self.to_dict())

    ##############################################

    def update_path(self, file_path):

        # Fixme: .shasum
        if file_path.compute_shasum() == self.shasum:
            self.path = file_path
            self.inode = file_path.inode
            self.update_record_date()
        else:
            raise NameError("Attempt to update a document path with a document having different shasum")

    ##############################################

    def update_shasum(self):

        self.shasum = self.path.compute_shasum() # Fixme: .shasum
        self.update_record_date()
