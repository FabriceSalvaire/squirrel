####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

####################################################################################################

SqlAlchemyBase = declarative_base()

####################################################################################################

from Babel.DataBase.SqlAlchemyBase import (SqlRow, SqlTable, SqlTableModel, ColumnWidthFactory)
from Babel.DataBase.SqliteDataBase import SqliteDataBase

####################################################################################################

class FileRow(SqlAlchemyBase, SqlRow):

    __tablename__ = 'files'

    path = Column(String, primary_key=True)
    shasum = Column(String, primary_key=True) # type ?
    inode = Column(Integer)
    creation_time = Column(Integer)

    ##############################################
        
    def __repr__(self):
        
        message = '''
File Row
  path: %(path)s
  shasum: %(shasum)s
  inode: %(inode)u
  creation time: %(creation_time)u
'''
        return message % self.get_column_dict()

    ##############################################

    def update(self, file_path):

        if self.path != str(file_path):
            raise NameError("Attempt to update with a different path")
        self.shasum = file_path.shasum
        self.inode = file_path.inode
        self.creation_time = file_path.creation_time

####################################################################################################

class FileSqlTable(SqlTable):

    ROW_CLASS = FileRow

    ##############################################

    def add(self, file_path):

        file_row = self.ROW_CLASS(path=str(file_path),
                                  shasum=file_path.shasum,
                                  inode=file_path.inode,
                                  creation_time=file_path.creation_time)
        self._session.add(file_row)

####################################################################################################

class FileDataBase(SqliteDataBase):
    
    __base__ = SqlAlchemyBase

    ##############################################
    
    def __init__(self, filename, echo=False):

        super(FileDataBase, self).__init__(filename, echo)

        self.file_table = FileSqlTable(self)

####################################################################################################
# 
# End
# 
####################################################################################################
