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

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref

from Babel.Corpus.LanguageId import LanguageId
from ..SqlAlchemyBase import SqlRow, SqlTable
from ..Types.Choice import ChoiceType

####################################################################################################

class DocumentWordRowMixin(SqlRow):

    # Fixme: RowMixin -> Mixin
    # Fixme: ...s ?

    __tablename__ = 'document_words'

    count = Column(Integer)
    rank = Column(Integer)

    ##############################################

    @declared_attr
    def document_id(cls):
        return Column(Integer, ForeignKey('documents.id'), primary_key=True, index=True)

    @declared_attr
    def word_id(cls):
        return Column(Integer, ForeignKey('words.id'), primary_key=True, index=True)

    ##############################################

    def __repr__(self):

        message = '''
Document Word Row
  document: {0.document_id}
  word: {0.word_id}
'''
        return message.format(self)

####################################################################################################

class WordRowMixin(SqlRow):

    __tablename__ = 'words'

    # indexed word global: id, language, word, count <to learn new word>

    id = Column(Integer, primary_key=True)

    word = Column(String) # Fixme: uniq ?
    language = Column(ChoiceType(LanguageId), default=0) # ForeignKey

    ##############################################

    # DOCUMENT_WORD_TABLE_CLS = None

    @declared_attr
    def documents(cls):
        # secondary=cls.DOCUMENT_WORD_TABLE_CLS
        return relationship('DocumentRow', secondary='document_words', back_populates='words')

    ##############################################

    def __repr__(self):

        message = '''
Word Row
  word: {0.word}
'''
        return message.format(self)
