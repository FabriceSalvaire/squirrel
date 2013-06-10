####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

from sqlalchemy import Column, Boolean, Integer, String
from sqlalchemy.ext.declarative import declarative_base

####################################################################################################

SqlAlchemyBase = declarative_base()

####################################################################################################

from Babel.DataBase.SqlAlchemyBase import SqlRow, SqlTable
from Babel.DataBase.SqliteDataBase import SqliteDataBase

####################################################################################################

class WordRow(SqlAlchemyBase, SqlRow):

    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    word = Column(String) # , primary_key=True
    document_id = Column(Integer) # , primary_key=True
    count = Column(Integer, default=0)

    ##############################################
        
    def __repr__(self):
        
        message = '''
Word Row
  word: %(word)s
  document id: %(document_id)u
  count: %(count)u
'''
        return message % self.get_column_dict()

####################################################################################################

class WordSqlTable(SqlTable):

    ROW_CLASS = WordRow

####################################################################################################

class WordDocumentDataBase(SqliteDataBase):
    
    __base__ = SqlAlchemyBase

    ##############################################
    
    def __init__(self, filename, echo=False):

        super(WordDocumentDataBase, self).__init__(filename, echo)

        self.word_table = WordSqlTable(self)

####################################################################################################
# 
# End
# 
####################################################################################################
