# -*- coding: utf-8 -*-

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

from PyQt4 import QtGui

####################################################################################################

class ImagePage(QtGui.QScrollArea):

    ##############################################

    def __init__(self, main_window):

        super(ImagePage, self).__init__()

        self._main_window = main_window
        self._init_ui()

    ##############################################

    def _init_ui(self):

        # self._scroll_area = QtGui.QScrollArea(self)
        self.setWidgetResizable(True)
        self._pixmap_label = QtGui.QLabel()
        # self.setWidget(self._pixmap_label)

        widget = QtGui.QWidget()
        horizontal_layout = QtGui.QHBoxLayout(widget)
        spacer_item1 = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        spacer_item2 = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        horizontal_layout.addItem(spacer_item1)
        horizontal_layout.addWidget(self._pixmap_label)
        horizontal_layout.addItem(spacer_item2)
        self.setWidget(widget)

    ##############################################

    def update_page(self):

        pdf_page = self._main_window._pdf_page
        np_array = pdf_page.to_pixmap()
        height, width = np_array.shape[:2]
        image = QtGui.QImage(np_array.data, width, height, QtGui.QImage.Format_ARGB32)
        self._pixmap_label.setPixmap(QtGui.QPixmap.fromImage(image))

####################################################################################################
#
# End
#
####################################################################################################
