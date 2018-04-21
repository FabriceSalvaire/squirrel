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

from pathlib import Path
import logging

from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class QmlPathNavigator(QObject):

    _logger = _module_logger.getChild('QmlPathNavigator')

    path_changed = pyqtSignal(Directory)

    ##############################################

    def __init__(self, parent=None, path=None):

        super().__init__(parent)

        self._path = None
        if path is not None:
            self.path = path

    ##############################################

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._set_path(path, emit=False)

    ##############################################

    path_str_changed = pyqtSignal()

    @pyqtProperty('QString', notify=path_str_changed)
    def path_str(self):
        return self._path

    @path_str.setter
    def path_str(self, path):
        self._set_path(path, emit=False)

    ##############################################

    def _set_path(self, path, emit=True):

        self._path = Path(path)

        if emit:
            self.path_changed.emit(self._path)

    ##############################################

    path_parts_changed = pyqtSignal()

    @pyqtProperty('QStringList', notify=path_parts_changed)
    def path_parts(self):
        return self._path.parents

    ##############################################

    @pyqtSlot()
    def directory_list(self):

        directories = sorted([directory.basename() for directory in self._path.XXX()],
                             key=lambda x: x.lower())
        return directory
