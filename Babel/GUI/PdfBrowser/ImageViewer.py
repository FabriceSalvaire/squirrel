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

import logging
import os
import subprocess

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

####################################################################################################

from Babel.Tools.EnumFactory import EnumFactory

####################################################################################################

_module_logger = logging.getLogger(__name__)
      
####################################################################################################

class ImageViewer(QtGui.QScrollArea):

    _logger = _module_logger.getChild('ImageViewer')

    zoom_mode_enum = EnumFactory('ZoomModeEnum', ('fit_document', 'fit_width'))

    # Fixme
    horizontal_margin = 40 # scroller width
    vertical_margin = 15 # widget margin?

    ##############################################

    def __init__(self, main_window):

        super(ImageViewer, self).__init__()

        self._main_window = main_window
        self._init_ui()

        self._document = None
        self._zoom_mode = None

    ##############################################

    def _init_ui(self):

        self.setWidgetResizable(True)

        self.setWidgetResizable(True)
        self._pixmap_label = QtGui.QLabel()
        self._pixmap_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setWidget(self._pixmap_label)

    ##############################################

    def update(self, document):

        self._document = document
        self.fit_document()

    ##############################################

    def update_style(self):

        if self._document.selected:
            margin = 15
            colour = QtGui.QColor()
            colour.setHsv(210, 150, 250)
        else:
            margin = 0
            colour = QtGui.QColor(Qt.white)
        self._pixmap_label.setStyleSheet("border: {}px solid {};".format(margin, colour.name()))

    ##############################################

    def fit_width(self):

        self._logger.info('')
        # Fixme: resolution versus dimension
        self._zoom_mode = self.zoom_mode_enum.fit_width
        image = self._document.load(width=self.width() -self.horizontal_margin,
                                    height=0,
                                    resolution=1000)
        self._set_pixmap(image)

    ##############################################

    def fit_document(self):

        self._logger.info('')
        self._zoom_mode = self.zoom_mode_enum.fit_document
        image = self._document.load(width=self.width() -self.horizontal_margin,
                                    height=self.height() -self.vertical_margin,
                                    resolution=1000)
        self._set_pixmap(image)

    ##############################################

    def _set_pixmap(self, image):

        self.update_style()
        height, width = image.shape[:2]
        qimage = QtGui.QImage(image.data, width, height, QtGui.QImage.Format_ARGB32)
        self._pixmap_label.setPixmap(QtGui.QPixmap.fromImage(qimage))

    ##############################################

    def clear(self):

        self._pixmap_label.clear()

    ##############################################

    def resizeEvent(self, event):

        # self._logger.info('')
        if self._zoom_mode == self.zoom_mode_enum.fit_document:
            self.fit_document()
        else:
            self.fit_width()
            
####################################################################################################
#
# End
#
####################################################################################################
