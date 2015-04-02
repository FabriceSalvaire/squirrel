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

from sqlalchemy import Index
from sqlalchemy.ext.declarative import declarative_base

####################################################################################################

from ..SqlAlchemyBase import SqlTable
from ..SqliteDataBase import SqliteDataBase

####################################################################################################

class DocumentSqliteDataBase(SqliteDataBase):
    
    ##############################################
    
    def __init__(self, filename, echo=False):

        super(DocumentSqliteDataBase, self).__init__(filename, echo)

        self._declarative_base_class = declarative_base()

        from .DocumentTable import DocumentRowMixin, DocumentTableMixin
        self._document_row_class = type('DocumentRow', (DocumentRowMixin, self._declarative_base_class), {})
        self._document_table_class = type('DocumentTable', (DocumentTableMixin, SqlTable),
                                          {'ROW_CLASS':self._document_row_class})
        self.document_table = self._document_table_class(self)

        from .WordTable import WordRowMixin
        self._word_row_class = type('WordRow', (WordRowMixin, self._declarative_base_class), {})
        self._word_table_class = type('WordTable', (SqlTable,), {'ROW_CLASS':self._word_row_class})
        self.word_table = self._word_table_class(self)

        if self.create():
            # self._create_indexes(analysis)
            pass
        
    ##############################################
    
    # def _create_indexes(self, analysis):

    #     indexes = []
    #     if analysis:
    #         length = self._..._row_class.get_column('...')
    #         indexes += (
    #             Index('..._index', length.asc()),
    #             )

    #     for index in indexes:
    #         index.create(self._engine)
        
####################################################################################################
# 
# End
# 
####################################################################################################
