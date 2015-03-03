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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

####################################################################################################

from .DirectoryTocWidget import DirectoryTocWidget
from Babel.FileSystem.DirectoryToc import DirectoryToc
from Babel.GUI.Widgets.IconLoader import IconLoader
from Babel.GUI.Widgets.PathNavigator import PathNavigator

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class DirectorySelector(QtGui.QDialog):

    _logger = _module_logger.getChild('DirectorySelector')

    ##############################################

    def __init__(self, path):

        super(DirectorySelector, self).__init__()

        self.showMaximized()

        self._init_ui()

        self._open_directory(path)

    ##############################################

    def _open_directory(self, path):

        self._directory_toc.update(DirectoryToc(path))
        self._path_navigator.set_path(path) # Fixme: path_navigator -> open_directory -> path_navigator

    ##############################################

    def _init_ui(self):

        icon_loader = IconLoader()
        
        self._path_navigator = PathNavigator(self)
        self._directory_toc = DirectoryTocWidget()
        self._path_navigator.path_changed.connect(self._open_directory)
        self._directory_toc.path_changed.connect(self._open_directory)

        self._create_directory_button = QtGui.QPushButton('New', self)
        self._create_directory_button.setIcon(icon_loader['list-add'])
        self._create_directory_button.clicked.connect(self.create_directory)
        horizontal_layout = QtGui.QHBoxLayout()
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self._create_directory_button)

        self._vertical_layout = QtGui.QVBoxLayout(self)
        self._vertical_layout.addLayout(horizontal_layout)
        self._vertical_layout.addWidget(self._path_navigator)
        self._vertical_layout.addWidget(self._directory_toc)
        
        self._open_button = QtGui.QPushButton('Open')
        self._cancel_button = QtGui.QPushButton('Cancel')
        self._open_button.clicked.connect(self.accept)
        self._cancel_button.clicked.connect(self.reject)
        horizontal_layout = QtGui.QHBoxLayout()
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self._cancel_button)
        horizontal_layout.addWidget(self._open_button)
        self._vertical_layout.addLayout(horizontal_layout)

    ##############################################

    @property
    def path(self):
        return self._path_navigator.path

    ##############################################

    def keyPressEvent(self, event):

        print event.key()
        if event.key() == Qt.Key_Return:
            self.accept()
        else:
            super(DirectorySelector, self).keyPressEvent(event)

    ##############################################

    def create_directory(self):

        directory, ok = QtGui.QInputDialog.getText(self, "Create a directory", "Directory:")
        if ok:
            directory = unicode(directory)
            absolut_directory = self.path.join_directory(directory)
            try:
                self._logger.info("create directory {}".format(unicode(absolut_directory)))
                os.mkdir(unicode(absolut_directory))
                self._open_directory(self.path) # reload ?
            except Exception as exception:
                # Fixme: show message in main window
                self._logger.error(unicode(exception))
                application = QtGui.QApplication.instance()
                application.show_message(unicode(exception))
                
####################################################################################################
#
# End
#
####################################################################################################
