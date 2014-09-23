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
