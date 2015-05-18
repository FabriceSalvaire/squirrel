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

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref

####################################################################################################

from Babel.DataBase.SqlAlchemyBase import SqlRow

####################################################################################################

class WordRowMixin(SqlRow):

    __tablename__ = 'document_words'

    # indexed word global: id, language, word, count <to learn new word>
    
    id = Column(Integer, primary_key=True)
    language = Column(Integer, default=0) # ForeignKey, 0 = unknown, 1 = en ...
    word = Column(String)
    count = Column(Integer)
    rank = Column(Integer)

    ##############################################
        
    # document_id = Column(Integer, ForeignKey('documents.id'), index=True)
    ## sqlalchemy.exc.InvalidRequestError: Mapper properties (i.e. deferred,column_property(),
    ## relationship(), etc.) must be declared as @declared_attr callables on declarative mixin
    ## classes.
    # document = relationship('DocumentRowMixin', backref=backref('words', order_by=id))

    ###############################################

    @declared_attr
    def document_id(cls):
        return Column(Integer, ForeignKey('documents.id'), index=True)

    # @declared_attr
    # def document(cls):
    #     return relationship('DocumentRow', backref=backref('words', order_by=cls.id))
    
    ##############################################
        
    def __repr__(self):

        message = '''
Word Row
  word: {word}
  count: {count}
'''
        return message.format(**self.to_dict())

####################################################################################################
# 
# End
# 
####################################################################################################
