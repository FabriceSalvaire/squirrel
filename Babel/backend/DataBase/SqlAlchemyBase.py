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
import sqlalchemy
from sqlalchemy.inspection import inspect

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

def autoload_table(engine, table_name):

    metadata = sqlalchemy.MetaData()

    return sqlalchemy.Table(table_name, metadata, autoload=True, autoload_with=engine)

####################################################################################################

class SqlRow:

    __table__ = None

    ##############################################

    @classmethod
    def column_names(cls, only_known=False):

        mapper = inspect(cls)
        # Wrong: return mapper.attrs.keys()
        if only_known:
            return [column.name for column in mapper.columns
                    if 'unknown' in column.info and column.info['unknown']]
        else:
            return mapper.columns.keys()

    ###############################################

    @classmethod
    def get_column(cls, column):

        mapper = inspect(cls)
        # or mapper.columns.column
        return mapper.columns[column]

    ###############################################

    @classmethod
    def field_title(cls, field):

        info = cls.get_column(field).info
        return info.get('title', '')

    ###############################################

    @classmethod
    def field_width(cls, field):

        info = cls.get_column(field).info
        return info.get('width', None)

    ##############################################

    def to_dict(self, only_known=False):

        return {column:getattr(self, column) for column in self.column_names(only_known)}

    ###############################################

    def to_clone_dict(self):

        d = self.to_dict()
        del d['id']

        return d

    ###############################################

    def clone(self):

        return self.__class__(**self.to_clone_dict())

####################################################################################################

class SqlTable:

    ROW_CLASS = None

    _logger = _module_logger.getChild('.SqlTable')

    ##############################################

    def __init__(self, database):

        # Fixme: database vs session ?

        self._database = database
        self._session = database.session

    ###############################################

    def commit(self):

        self._session.commit()

    ###############################################

    def merge(self, obj):

        return self._session.merge(obj)

    ###############################################

    def new_row(self, *args, **kwargs):

        return self.ROW_CLASS(*args, **kwargs)

    ###############################################

    def add(self, row, commit=False):

        self._session.add(row)
        if commit:
            self.commit()

    ###############################################

    def add_new_row(self, *args, **kwargs):

        # Fixme: commit

        row = self.new_row(*args, **kwargs)
        self.add(row)
        return row

    ###############################################

    def query(self):

        # Close session else data are cached by the transaction ?
        # /!\ converted = True doesn't work anymore
        # self._session.close()

        return self._session.query(self.ROW_CLASS)

    ##############################################

    def all(self):

        return self.query().all()

    ###############################################

    def filter(self, where_clause):

        return self.query().filter(where_clause)

    ###############################################

    def filter_by(self, **kwargs):

        return self.query().filter_by(**kwargs)

####################################################################################################

class ColumnWidthFactory:

    ##############################################

    def  __init__(self, template='M', factor=1):

        self._template = template
        self._factor = factor

    ##############################################

    def  __call__(self, font_metrics):

        return self._factor * font_metrics.width(self._template)

####################################################################################################

class ColumnDateWidthFactory(ColumnWidthFactory):

    ##############################################

    def  __init__(self, factor=1):

        super(ColumnDateWidthFactory, self).__init__(template='x7777-77-77 77:77:77x', factor=factor)
