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

from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

from Babel.Config import ConfigInstall
from Babel.Corpus import tag_registry
from ..SqlAlchemyBase import SqlRow, SqlTable
from ..SqliteDataBase import SqliteDataBase

####################################################################################################

class WordMixin(SqlRow):

    __tags__  = None

    id = Column(Integer, primary_key=True)

    word = Column(String, unique=True, nullable=False)
    tags1 = Column(Integer)
    frequency = Column(Integer)
    rank = Column(Integer)

    ##############################################

    @declared_attr
    def lemma_id(cls):
        return Column(Integer, ForeignKey(cls.__tablename__ + '.id'), nullable=True)

    @declared_attr
    def lemmas(cls):
        return relationship(cls.__name__, backref=backref('lemma', remote_side=[cls.id]))

    ##############################################

    @hybrid_property
    def tags(self):
        return self.tags1,

    ##############################################

    def __repr__(self):

        message = '''
Word Row
  word: {0.word}
  part of speech tags: {0.tags}
  rank: {0.rank}
  frequency: {0.frequency}
  lemma: {0.lemma_id}
'''
        return message.format(self)

####################################################################################################

class WordExtendedPosMixin(WordMixin):

    tags2 = Column(Integer)

    ##############################################

    @hybrid_property
    def tags(self):
        return self.tags1, self.tags2

####################################################################################################

class CorpusSqliteDataBase(SqliteDataBase):

    ##############################################

    @classmethod
    def create_schema_classes(cls, languages):

        declarative_base_cls = declarative_base()

        row_classes = {}
        table_classes = {}

        for language in languages:
            tags = tag_registry[language]
            table_name = 'corpus_' + language
            Language = language.title()
            mixin = WordExtendedPosMixin if tags.require_extended_tag else WordMixin
            word_row_cls = type('WordRow' + Language, (mixin, declarative_base_cls), {
                '__tablename__': table_name,
                '__tags__': tags,
            })
            word_table_cls = type('WordTable' + Language, (SqlTable,), {
                'ROW_CLASS': word_row_cls,
            })
            row_classes[table_name] = word_row_cls
            table_classes[table_name] = word_table_cls

        return declarative_base_cls, row_classes, table_classes

    ##############################################

    def __init__(self, filename, echo=False):

        super().__init__(filename, echo)

        # Language ID are defined in Corpus.LanguageID
        languages = ConfigInstall.Corpus.languages
        self.init_schema(languages)

        if self.create():
            # self._create_indexes(analysis)
            pass
