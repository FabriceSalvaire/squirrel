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

import datetime
today = datetime.datetime.today

from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

####################################################################################################

from Babel.Corpus.LanguageId import LanguageId
from ..SqlAlchemyBase import SqlRow
from ..Types.Choice import ChoiceType
from ..Types.Path import FileType

####################################################################################################

class DocumentRowMixin(SqlRow):

    __tablename__ = 'documents'

    # Record ID
    id = Column(Integer, primary_key=True)
    record_creation_date = Column(DateTime)
    record_update_date = Column(DateTime)

    # Document key, note duplicates are allowed
    shasum = Column(String(64))
    has_duplicate = Column(Boolean, default=False)

    # Other document key
    # root_path
    path = Column(FileType, unique=True)
    inode = Column(Integer) # uniq on the same file-system
    # creation_time = Column(Integer)

    # Document Metadata
    author = Column(String, default='')
    language = Column(ChoiceType(LanguageId), default=0) # ForeignKey
    number_of_pages = Column(Integer)
    title = Column(String, default='')

    # User classification
    comment = Column(String, default='')
    keywords = Column(String, default='')
    star = Column(Integer, default=0)
    dewey = Column(Float, default=0) # Dewey classification 'xyz.abc de' = float xyz.abcde
    # classification = ... # Fixme: how ?

    # Index
    # Fixme: emplain more ???
    indexation_date = Column(DateTime, default=None) # to compare with indexer generation
    indexed_until = Column(Integer, default=0) # should be equal to number_of_pages
                                               # page number start from 1, 0 means not indexed
    indexation_status = Column(String, default='') # Fixme:
    # indexer settings

    # Fixme:
    #  - manage a root cache
    #  - split file_path
    #  - manage filter_by path

    # @declared_attr
    # def document_root_id(cls):
    #     return Column(Integer, ForeignKey('document_roots.id'), index=True)

    ##############################################

    def __init__(self, job):

        self.record_creation_date = today()
        self.update_record_date()
        self.path = str(job.relative_path)
        self.inode = job.path.inode
        self.shasum = job.shasum

    ##############################################

    def update_record_date(self):
        self.record_update_date = today()

    ##############################################

    def update_indexation_date(self):
        self.indexation_date = today()

    ###############################################

    # DOCUMENT_WORD_TABLE_CLS = None

    @declared_attr
    def words(cls):
        return relationship('WordRow', secondary='document_words', back_populates='documents')

    ##############################################

    def __repr__(self):

        message = '''
Document Row
  path: {0.path}
  shasum: {0.shasum}
  inode: {0.inode}
  record date: {0.record_creation_date}
  update date: {0.record_update_date}
  number of pages: {0.number_of_pages}
  title: {0.title}
  author: {0.author}
  comment: {0.comment}
'''

        return message.format(self)

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
