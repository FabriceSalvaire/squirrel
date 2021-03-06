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

import logging

from sqlalchemy import Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

from Babel.backend.Corpus.LanguageId import LanguageId
from ..ServerDatabase import ServerDatabase
from ..SqlAlchemyBase import SqlTable
from ..SqliteDatabase import SqliteDatabase

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class DocumentDatabase(SqliteDatabase):

    _logger = _module_logger.getChild('DocumentDatabase')

    ##############################################

    @classmethod
    def create_schema_classes(cls):

        cls._logger.debug('')

        declarative_base_cls = declarative_base()

        from .WordTable import WordRowMixin, DocumentWordRowMixin
        from .DocumentTable import DocumentRowMixin
        from .LogTable import ImporterLogRowMixin

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

        importer_log_row_cls = type('ImporterLogRow', (ImporterLogRowMixin, declarative_base_cls), {})
        importer_log_table_cls = type('ImporterLogTable', (SqlTable,), {
            'ROW_CLASS': importer_log_row_cls,
        })

        row_classes = {
            'document':document_row_cls,
            'document_word':document_word_row_cls,
            'word':word_row_cls,
            'importer_log':importer_log_row_cls,
        }

        table_classes = {
            'document':document_table_cls,
            'document_word':document_word_table_cls,
            'word':word_table_cls,
            'importer_log':importer_log_table_cls,
        }

        return declarative_base_cls, row_classes, table_classes

    ##############################################

    def add_words_for_document(self, document_row, words):

        word_rows = []
        for word_count in words:
            word_entry = word_count.word_entry
            if word_entry is None:
                language = LanguageId.unknown
            else:
                language = word_entry.language
            try:
                word_row = self.word_table.filter_by(language=language, word=word_count.word).one() # or .one_or_none()
            except NoResultFound:
                word_row = self.word_table.add_new_row(language=language, word=word_count.word)
            word_rows.append(word_row)
        self.word_table.commit()

        for word_count, word_row in zip(words, word_rows):
            self.document_word_table.add_new_row(
                document_id=document_row.id,
                word_id=word_row.id,
                count=word_count.count,
                rank=word_count.rank,
            )
        self.document_word_table.commit()

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

class DocumentSqliteDatabase(DocumentDatabase, SqliteDatabase):

    ##############################################

    def __init__(self, filename, echo=False):

        super().__init__(filename, echo)

        self.init_schema()

        if self.create():
            # self._create_indexes(analysis)
            pass

####################################################################################################

class DocumentServerDatabase(DocumentDatabase, ServerDatabase):

    ##############################################

    def __init__(self, database_config, echo=False):

        super().__init__(database_config, echo)

        self.init_schema()

        if self.create():
            # self._create_indexes(analysis)
            pass

####################################################################################################

def open_database(database_config):

    if database_config.driver == 'sqlite':
        return DocumentSqliteDatabase(database_config.document_database())
    else:
        return DocumentServerDatabase(database_config)
