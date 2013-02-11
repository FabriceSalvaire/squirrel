####################################################################################################

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

####################################################################################################

SqlAlchemyBase = declarative_base()

####################################################################################################

class FileRow(SqlAlchemyBase):

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
    
    @classmethod
    def column_names(cls):

        return [column.name for column in cls.__table__.columns]

    ##############################################
    
    def get_column_dict(self):

        return {column:getattr(self, column) for column in self.column_names()}

####################################################################################################

class FileDataBase(object):

    ##############################################

    def __init__(self, sqlite_filename, echo=False):

        connection_str = "sqlite:///" + sqlite_filename
        self._engine = create_engine(connection_str, echo=echo)
        Session = sessionmaker(bind=self._engine)
        self._session = Session()

        SqlAlchemyBase.metadata.create_all(self._engine)

    ##############################################

    def add(self, file_path):

        file_row = FileRow(path=str(file_path),
                           shasum=file_path.shasum,
                           inode=file_path.inode,
                           creation_time=file_path.creation_time)
        self._session.add(file_row)

    ###############################################

    def commit(self):

        self._session.commit()

    ###############################################

    def query(self):

        return self._session.query(FileRow)

    ###############################################

    def select_by(self, **kwargs):

        filters = [getattr(FileRow, key) == value
                   for key, value in kwargs.items()]

        return self.query().filter(*filters)

####################################################################################################
# 
# End
# 
####################################################################################################
