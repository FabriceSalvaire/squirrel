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

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtProperty, QObject
from PyQt5.QtGui import QPalette

####################################################################################################

class ApplicationStyle(QObject):

    ##############################################

    def __init__(self):

        super().__init__()

        application = QtWidgets.QApplication.instance()

        # palette = QtWidgets.QStyle.standardPalette()
        palette = application.palette()

        self._window_color = palette.color(QPalette.Window)

    ##############################################

    @pyqtProperty('QColor', constant=True)
    def window_color(self):
        return self._window_color
