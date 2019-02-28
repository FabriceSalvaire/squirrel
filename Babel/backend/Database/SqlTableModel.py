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

import sqlalchemy

####################################################################################################

from PyQt5 import QtCore

####################################################################################################

class SqlTableModel(QtCore.QAbstractTableModel):

    ##############################################

    def __init__(self, sql_table):

        super(SqlTableModel, self).__init__()

        self._sql_table = sql_table

        self._columns = self._sql_table.ROW_CLASS.column_names() # Fixme: ?
        self._rows = []
        self._query = None
        self._sort_order = None

    ##############################################

    def __getitem__(self, _slice):

        return self._rows[_slice]

    ##############################################

    def _get_row_class(self):

        return self._sql_table.ROW_CLASS

    row_class = property(_get_row_class)

    ##############################################

    def _sort(self):

        if self._query is None:
            return

        if self.sorted():
            if self._sort_order == QtCore.Qt.AscendingOrder:
                query = self._query.order_by(self._sorted_column)
            else:
                query = self._query.order_by(sqlalchemy.desc(self._sorted_column))
        else:
            query = self._query
        self._rows = query.all() # Could return a huge list /!\
        self.reset()

    ##############################################

    def sort(self, column_index, order):

        column_name = self._columns[column_index]
        column = self.row_class.get_column(column_name) # Fixme: ?
        self._sorted_column = column
        self._sort_order = order
        self._sort()

    ##############################################

    def sorted(self):

        return self._sort_order is not None

    ##############################################

    def data(self, index, role=QtCore.Qt.DisplayRole):

        # Fixme: why ?
        if not index.isValid():
            return QtCore.QVariant()

        if role == QtCore.Qt.DisplayRole:
            try:
                row = self._rows[index.row()]
                column = self._columns[index.column()]
            except:
                return QtCore.QVariant()
            return QtCore.QVariant(str(getattr(row, column)))

        return QtCore.QVariant ()

    ##############################################

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):

        if role == QtCore.Qt.TextAlignmentRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QVariant(int(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
            else:
                return QtCore.QVariant(int(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter))

        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                column_name = self._columns[section]
                title = self.row_class.field_title(column_name) # Fixme: ?
                return QtCore.QVariant(title)
            else:
                return QtCore.QVariant(section)

        return QtCore.QVariant()

    ##############################################

    def set_column_widths(self, table_view):

        font_metrics = table_view.fontMetrics()
        for column_index, column_name in enumerate(self._columns):
            width_title = font_metrics.width('M'*2 + self.row_class.field_title(column_name))
            width_factory = self.row_class.field_width(column_name)
            if width_factory is not None:
                width = max(width_factory(font_metrics), width_title)
            else:
                width = width_title
            table_view.setColumnWidth(column_index, width)

    ##############################################

    def columnCount(self, index=QtCore.QModelIndex()):

        return len(self._columns)

    ##############################################

    def rowCount(self, index=QtCore.QModelIndex()):

        return len(self._rows)

    ##############################################

    def column_index(self, column):

        return self._columns.index(column)

    ##############################################

    def all(self):

        self._query = self._sql_table.query()
        self._sort()

    ##############################################

    def filter_by(self, **kwargs):

        self._query = self._sql_table.filter_by(**kwargs)
        self._sort()

    ##############################################

    def filter(self, where_clause):

        self._query = self._sql_table.filter(where_clause)
        self._sort()

    ##############################################

    def index_of(self, row):

        try:
            index = self._rows.index(row)
            return self.index(index, 0)
        except:
            return None
