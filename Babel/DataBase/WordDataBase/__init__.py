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

from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

####################################################################################################

SqlAlchemyBase = declarative_base()

####################################################################################################

from Babel.DataBase.SqlAlchemyBase import SqlRow, SqlTable
from Babel.DataBase.SqliteDataBase import SqliteDataBase

####################################################################################################

class LanguageRow(SqlAlchemyBase, SqlRow):

    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    name = Column(Integer)
    # international code ?

    ##############################################
        
    def __repr__(self):
        
        message = '''
Language Row
  id: %(id)u
  language: %(name)s
'''
        return message % self.get_column_dict()

####################################################################################################

class LanguageTable(SqlTable):

    ROW_CLASS = LanguageRow

####################################################################################################

class PartOfSpeechTagRow(SqlAlchemyBase, SqlRow):

    __tablename__ = 'part_of_speech_tags'

    id = Column(Integer, primary_key=True)
    tag = Column(String)
    comment = Column(String)

    ##############################################
        
    def __repr__(self):
        
        message = '''
Part-Of-Speech Tags Row
  id: %(id)u
  tag: %(tag)s
  comment: %(comment)s
'''
        return message % self.to_dict()

####################################################################################################

class PartOfSpeechTagTable(SqlTable):

    ROW_CLASS = PartOfSpeechTagRow

####################################################################################################

class WordRow(SqlAlchemyBase, SqlRow):

    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    word = Column(String) # , primary_key=True
    # language_id = Column(Integer, ForeignKey('languages.id'))
    part_of_speech_tag_id = Column(Integer) #, ForeignKey('part_of_speech_tags.id')) # Fixme: tag_id
    count = Column(Integer, default=0)
    file_count = Column(Integer, default=0) # Fixme: purpose ?
    rank = Column(Integer, default=0) # Fixme: purpose ?

    # language = relationship('LanguageRow')

    ##############################################
        
    def __repr__(self):

#   language id: %(language_id)u
#   common: %(common)s
        
        message = '''
Word Row
  word: %(word)s
  count: %(count)u
  part of speech tag: %(part_of_speech_tag_id)u
'''
        return message % self.to_dict()

####################################################################################################

class WordTable(SqlTable):

    ROW_CLASS = WordRow

####################################################################################################

class WordSqliteDataBase(SqliteDataBase):
    
    __base__ = SqlAlchemyBase

    ##############################################
    
    def __init__(self, filename, echo=False):

        super(WordSqliteDataBase, self).__init__(filename, echo)

        self.language_table = LanguageTable(self)
        self.part_of_speech_tag_table = PartOfSpeechTagTable(self)
        self.word_table = WordTable(self)

####################################################################################################
# 
# End
# 
####################################################################################################
