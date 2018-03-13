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

"""This module implements a list widget where items are made of a label and a delete icon.

"""

# Fixme:
#  see DirectoryList.qml for QML port
#  Must be generic
#  MVC list model and item delegate

####################################################################################################

import logging
import os

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal

from Babel.FileSystem.File import Directory, File
from Babel.Tools.IterTools import pairwise
from ..Widgets.IconLoader import IconLoader
from .DirectorySelector import DirectorySelector

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

icon_loader = IconLoader()

####################################################################################################

class DirectoryWidget(QtWidgets.QWidget):

    """Implement a widget made of a label and a delete icon.

    """

    _logger = _module_logger.getChild('DirectoryWidget')

    deleted = pyqtSignal(QtWidgets.QWidget)
    dropped_file = pyqtSignal(File, Directory)
    move_current_file = pyqtSignal(Directory)

    ##############################################

    def __init__(self, path, parent=None):

        super().__init__(parent)

        self._path = path

        self.setToolTip(str(path))

        self._delete_button = QtWidgets.QToolButton(self)
        self._delete_button.setIcon(icon_loader['delete-black@36'])
        self._delete_button.setAutoRaise(True)

        # self._label = QtWidgets.QLabel(self)
        self._label = QtWidgets.QPushButton(self)
        self.set_label_level()

        self._horizontal_layout = QtWidgets.QHBoxLayout(self)
        self._horizontal_layout.addWidget(self._delete_button)
        self._horizontal_layout.addWidget(self._label)

        self._delete_button.clicked.connect(lambda x: self.deleted.emit(self))
        self._label.clicked.connect(lambda x: self.move_current_file.emit(self._path))

        self.setAcceptDrops(True)

    ##############################################

    def same_path(self, path):
        return self._path == path

    ##############################################

    def label(self):
        return self._label.text()

    ##############################################

    def has_same_label(self, other):
        return self.label() == other.label()

    ##############################################

    def set_label_level(self, level=1):

        if level == 1:
            label = self._path.basename()
        else:
            sep = os.path.sep
            label = sep.join(self._path.split()[-level:])
        self._label.setText(label)

    ##############################################

    def update_label_for_collision(self, other):

        level = self._path.reverse_level_of_equality(other._path) +1
        self.set_label_level(level)
        other.set_label_level(level)

    ##############################################

    def dragEnterEvent(self, event):

        # Fixme: usefull ? click is easier !

        self._logger.info('')
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            urls = [str(url.path()) for url in mime_data.urls()]
            self._logger.info(str(self._path) + ' ' + str(urls[0]))
            if File(urls[0]).directory != self._path:
                self.setBackgroundRole(QtGui.QPalette.Highlight)
                event.acceptProposedAction() # mandatory

    ##############################################

    def dragLeaveEvent(self, event):

        self._logger.info('')
        self.setBackgroundRole(QtGui.QPalette.Window)
        event.accept()

    ##############################################

    # def dragMoveEvent(self, event):

        # self._logger.info('')
        # event.acceptProposedAction()

    ##############################################

    def dropEvent(self, event):

        mime_data = event.mimeData()
        if mime_data.hasUrls():
            urls = [str(url.path()) for url in mime_data.urls()]
            self._logger.info(str(urls))
            self.dropped_file.emit(File(urls[0]), self._path)
            self.setBackgroundRole(QtGui.QPalette.Window)
            event.acceptProposedAction()

####################################################################################################

class DirectoryListWidget(QtWidgets.QWidget):

    """Implement a list view"""

    _logger = _module_logger.getChild('DirectoryListWidget')

    move_file = pyqtSignal(File, Directory)
    move_current_file = pyqtSignal(Directory)

    ##############################################

    def __init__(self, parent=None):

        super().__init__(parent)

        self._application = QtWidgets.QApplication.instance()
        self._last_path = None

        self.setMinimumSize(200, 300)

        self._widgets = []

        vertical_layout = QtWidgets.QVBoxLayout(self)

        self._clear_button = QtWidgets.QToolButton(self)
        self._clear_button.setToolTip('Remove all destinations')
        self._clear_button.setIcon(icon_loader['delete-black@36'])
        self._clear_button.setAutoRaise(True)

        self._add_button = QtWidgets.QToolButton(self)
        self._add_button.setToolTip('Add a destination')
        self._add_button.setIcon(icon_loader['playlist-add-black@36'])
        self._add_button.setAutoRaise(True)

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addStretch()
        horizontal_layout.addWidget(self._add_button)
        horizontal_layout.addWidget(self._clear_button)
        vertical_layout.addLayout(horizontal_layout)

        self._scroll_area = QtWidgets.QScrollArea(self)
        self._scroll_area.setWidgetResizable(True)
        vertical_layout.addWidget(self._scroll_area)
        self._widget = QtWidgets.QWidget(self)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self._scroll_area.setSizePolicy(size_policy)
        self._vertical_layout = QtWidgets.QVBoxLayout(self._widget)
        self._vertical_layout.addStretch()
        self._scroll_area.setWidget(self._widget)

        self._add_button.clicked.connect(self.add)
        self._clear_button.clicked.connect(self.clear)

    ##############################################

    def add(self):

        self._logger.info('')

        # options = (QtWidgets.QFileDialog.ShowDirsOnly |
        #            QtWidgets.QFileDialog.DontUseNativeDialog |
        #            QtWidgets.QFileDialog.DontResolveSymlinks)
        # path = QtWidgets.QFileDialog.getExistingDirectory(self,
        #                                               "Select directory",
        #                                               unicode(path),
        #                                               options)

        if self._last_path is None:
            path = self._application.main_window.current_path
        else:
            path = self._last_path
        directory_selector = DirectorySelector(path)
        if directory_selector.exec_():
            path = directory_selector.path
            if self._test_for_identity(path):
                widget = DirectoryWidget(path, self)
                widget.deleted.connect(self._delete_item)
                widget.dropped_file.connect(self.move_file)
                widget.move_current_file.connect(self.move_current_file)
                index = self._vertical_layout.count() -1
                self._vertical_layout.insertWidget(index, widget)
                self._widgets.append(widget)
                self._last_path = path.directory_part()
                self._update_label_for_collision()

    ##############################################

    def _test_for_identity(self, path):

        for widget in self._widgets:
            if widget.same_path(path):
                return False
        return True

    ##############################################

    def _update_label_for_collision(self):

        self._widgets.sort(key=lambda x: x.label())
        for widget1, widget2 in pairwise(self._widgets):
            if widget1.has_same_label(widget2):
                widget1.update_label_for_collision(widget2)

    ##############################################

    def clear(self):

        layout = self._vertical_layout
        while layout.count() > 1:
            widget = layout.takeAt(0).widget()
            widget.deleteLater()
        self._widgets = []

    ##############################################

    def _delete_item(self, widget):

        index = self._widgets.index(widget)
        # Fixme: .removeWidget(widget) ?
        widget = self._vertical_layout.takeAt(index).widget()
        widget.deleteLater()
        del self._widgets[index]
