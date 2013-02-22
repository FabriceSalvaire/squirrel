####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

####################################################################################################

SqlAlchemyBase = declarative_base()

####################################################################################################

from Babel.DataBase.SqlAlchemyBase import (SqlRow, SqlTable, SqlTableModel, ColumnWidthFactory)
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

class LanguageSqlTable(SqlTable):

    ROW_CLASS = LanguageRow

####################################################################################################

class WordRow(SqlAlchemyBase, SqlRow):

    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    word = Column(String) # , primary_key=True
    language_id = Column(Integer, ForeignKey('languages.id'))
    count = Column(Integer, default=0)
    common = Column(Boolean,default=False)

    # language = relationship('LanguageRow')

    ##############################################
        
    def __repr__(self):
        
        message = '''
Word Row
  word: %(word)s
  language id: %(language_id)u
  count: %(count)u
  common: %(common)s
'''
        return message % self.get_column_dict()

####################################################################################################

class WordSqlTable(SqlTable):

    ROW_CLASS = WordRow

####################################################################################################

class WordDataBase(SqliteDataBase):
    
    __base__ = SqlAlchemyBase

    ##############################################
    
    def __init__(self, filename, echo=False):

        super(WordDataBase, self).__init__(filename, echo)

        self.language_table = LanguageSqlTable(self)
        self.word_table = WordSqlTable(self)

####################################################################################################
# 
# End
# 
####################################################################################################
