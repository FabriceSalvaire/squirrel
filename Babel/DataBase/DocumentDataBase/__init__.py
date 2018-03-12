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

import logging

from sqlalchemy import Index
from sqlalchemy.ext.declarative import declarative_base

from ..SqlAlchemyBase import SqlTable
from ..SqliteDataBase import SqliteDataBase

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class DocumentSqliteDataBase(SqliteDataBase):

    _logger = _module_logger.getChild('DocumentSqliteDataBase')

    ##############################################

    @classmethod
    def build_tables(cls):

        cls._logger.debug('')

        declarative_base_cls = declarative_base()

        from .WordTable import WordRowMixin, DocumentWordRowMixin
        from .DocumentTable import DocumentRowMixin

        # Association table for document <-> word many-to-many relation
        document_word_row_cls = type('DocumentWordRow', (DocumentWordRowMixin, declarative_base_cls), {})
        document_word_table_cls = type('DocumentWordTable', (SqlTable,), {
            'ROW_CLASS':document_word_row_cls,
        })

        document_row_cls = type('DocumentRow', (DocumentRowMixin, declarative_base_cls), {
            # 'DOCUMENT_WORD_TABLE_CLS': document_word_table_cls,
        })
        document_table_cls = type('DocumentTable', (SqlTable,), {
            'ROW_CLASS': document_row_cls,
        })

        word_row_cls = type('WordRow', (WordRowMixin, declarative_base_cls), {
            # 'DOCUMENT_WORD_TABLE_CLS': document_word_table_cls,
        })
        word_table_cls = type('WordTable', (SqlTable,), {
            'ROW_CLASS': word_row_cls,
        })

        row_classes = {
            'document':document_row_cls,
            'document_word':document_word_row_cls,
            'word':word_row_cls,
        }

        table_classes = {
            'document':document_table_cls,
            'document_word':document_word_table_cls,
            'word':word_table_cls,
        }

        return declarative_base_cls, row_classes, table_classes

    ##############################################

    def __init__(self, filename, echo=False):

        super(DocumentSqliteDataBase, self).__init__(filename, echo)

        self._declarative_base_cls, row_classes, table_classes = self.build_tables()

        for name in row_classes:
            row_cls = row_classes[name]
            table_cls = table_classes[name]
            setattr(self, '_{}_row_class'.format(name), row_cls)
            setattr(self, '_{}_table_class'.format(name), table_cls)
            setattr(self, '{}_table'.format(name), table_cls(self))

        # self._document_row_class.DOCUMENT_WORD_TABLE_CLS = self._document_word_table_class
        # self._word_row_class.DOCUMENT_WORD_TABLE_CLS = self._document_word_table_class

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
