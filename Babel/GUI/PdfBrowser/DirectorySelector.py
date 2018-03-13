# -*- coding: utf-8 -*-

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

"""Implement a popup window to select a directory.

"""

# Fixme: port to QML

####################################################################################################

import logging
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt

from ..Widgets.IconLoader import IconLoader
from ..Widgets.PathNavigator import PathNavigator
from .DirectoryToc import DirectoryToc
from .DirectoryTocWidget import DirectoryTocWidget
from Babel.FileSystem.File import Directory

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class CreateDirectoryDialog(QtWidgets.QDialog):

    SELECT_RETURN_CODE = 2

    ##############################################

    def __init__(self, parent=None):

        super(CreateDirectoryDialog, self).__init__(parent)

        self.setWindowTitle("Create a directory")

        self._line_edit = QtWidgets.QLineEdit(self)
        self._line_edit.setMinimumSize(QtCore.QSize(300, 0))
        self._select_button = QtWidgets.QPushButton('Select', self)
        self._ok_button = QtWidgets.QPushButton('Ok', self)
        self._cancel_button = QtWidgets.QPushButton('Cancel', self)

        vertical_layout = QtWidgets.QVBoxLayout(self)
        vertical_layout.addWidget(self._line_edit)
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self._select_button)
        horizontal_layout.addWidget(self._ok_button)
        horizontal_layout.addWidget(self._cancel_button)
        vertical_layout.addLayout(horizontal_layout)

        self._select_button.clicked.connect(self.select)
        self._ok_button.clicked.connect(self.accept)
        self._cancel_button.clicked.connect(self.reject)

    ##############################################

    def value(self):
        return self._line_edit.text()

    ##############################################

    def select(self):
        self.done(self.SELECT_RETURN_CODE)

####################################################################################################

class DirectorySelector(QtWidgets.QDialog):

    _logger = _module_logger.getChild('DirectorySelector')

    ##############################################

    def __init__(self, path):

        super(DirectorySelector, self).__init__()

        self.showMaximized()

        self._init_ui()

        self._path = None
        self._open_directory(path)

    ##############################################

    def _open_directory(self, path):

        self._path = Directory(path)
        self._directory_toc.update(DirectoryToc(self._path))
        # Fixme: path_navigator -> open_directory -> path_navigator
        self._path_navigator.set_path(self._path)

    ##############################################

    def _init_ui(self):

        icon_loader = IconLoader()

        self._path_navigator = PathNavigator(self)
        self._directory_toc = DirectoryTocWidget()
        self._path_navigator.path_changed.connect(self._open_directory)
        self._directory_toc.path_changed.connect(self._open_directory)

        self._create_directory_button = QtWidgets.QPushButton('New', self)
        self._create_directory_button.setIcon(icon_loader['add-black@36'])
        self._create_directory_button.clicked.connect(self.create_directory)
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self._create_directory_button)

        self._vertical_layout = QtWidgets.QVBoxLayout(self)
        self._vertical_layout.addLayout(horizontal_layout)
        self._vertical_layout.addWidget(self._path_navigator)
        self._vertical_layout.addWidget(self._directory_toc)

        self._open_button = QtWidgets.QPushButton('Open')
        self._cancel_button = QtWidgets.QPushButton('Cancel')
        self._open_button.clicked.connect(self.accept)
        self._cancel_button.clicked.connect(self.reject)
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self._cancel_button)
        horizontal_layout.addWidget(self._open_button)
        self._vertical_layout.addLayout(horizontal_layout)

    ##############################################

    @property
    def path(self):
        return self._path

    ##############################################

    def keyPressEvent(self, event):

        print(event.key())
        if event.key() == Qt.Key_Return:
            self.accept()
        else:
            super(DirectorySelector, self).keyPressEvent(event)

    ##############################################

    def create_directory(self):

        # Fixme: mix ui and logic

        dialog = CreateDirectoryDialog(self)
        rc = dialog.exec_()
        if rc:
            directory = str(dialog.value())
            absolut_directory = self.path.join_directory(directory)
            try:
                self._logger.info("create directory {}".format(str(absolut_directory)))
                os.mkdir(str(absolut_directory))
                if rc == CreateDirectoryDialog.SELECT_RETURN_CODE:
                    self._path = absolut_directory
                    self.accept()
                else:
                     # Fixme: reload ?
                    self._open_directory(self.path)
            except Exception as exception:
                self._logger.error(str(exception))
                application = QtWidgets.QApplication.instance()
                application.show_message(str(exception), warn=True)
