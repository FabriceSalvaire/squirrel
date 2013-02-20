####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

from PyQt4 import QtCore, QtGui

####################################################################################################

class RowLayoutManager(object):

    """ This class implements a row layout manager. """

    ##############################################

    def __init__(self, grid_layout):

        self._grid_layout = grid_layout
        self.row = 0

    ##############################################

    def add_row(self, widgets):

        """ Add the widgets to the current row and go to to the next row.  If an item is :obj:`None`
        the column is skipped.
        """

        for i, widget in enumerate(widgets):
            if widget is not None:
                self._grid_layout.addWidget(widget, self.row, i)
        self.row += 1

####################################################################################################
# 
# End
# 
####################################################################################################
