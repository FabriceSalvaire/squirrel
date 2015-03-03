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

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal

####################################################################################################

from .DirectorySelector import DirectorySelector
from Babel.FileSystem.File import Directory, File
from Babel.GUI.Widgets.IconLoader import IconLoader

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class DirectoryWidget(QtWidgets.QWidget):

    _logger = _module_logger.getChild('DirectoryWidget')

    deleted = pyqtSignal(QtWidgets.QWidget)
    dropped_file = pyqtSignal(File, Directory)

    ##############################################

    def __init__(self, path, parent=None):

        super(DirectoryWidget, self).__init__(parent)

        self._path = path

        icon_loader = IconLoader()

        self._delete_button = QtWidgets.QToolButton(self)
        self._delete_button.setIcon(icon_loader['edit-delete'])
        self._delete_button.setAutoRaise(True)
        self._label = QtWidgets.QLabel(path.basename(), self)
        self._horizontal_layout = QtWidgets.QHBoxLayout(self)
        self._horizontal_layout.addWidget(self._delete_button)
        self._horizontal_layout.addWidget(self._label)

        self._delete_button.clicked.connect(lambda x: self.deleted.emit(self))

        self.setAcceptDrops(True)

    ##############################################

    def dragEnterEvent(self, event):

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

    _logger = _module_logger.getChild('DirectoryListWidget')

    move_file = pyqtSignal(File, Directory)

    ##############################################

    def __init__(self, parent=None):

        super(DirectoryListWidget, self).__init__(parent)

        self._application = QtWidgets.QApplication.instance()

        self._widgets = []
      
        icon_loader = IconLoader()

        vertical_layout = QtWidgets.QVBoxLayout(self)

        self._clear_button = QtWidgets.QPushButton('clear', self)
        self._add_button = QtWidgets.QToolButton(self)
        self._add_button.setIcon(icon_loader['list-add'])
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

        # Fixme:
        path = self._application._main_window._path_navigator.path
        # options = (QtWidgets.QFileDialog.ShowDirsOnly |
        #            QtWidgets.QFileDialog.DontUseNativeDialog |
        #            QtWidgets.QFileDialog.DontResolveSymlinks)
        # path = QtWidgets.QFileDialog.getExistingDirectory(self,
        #                                               "Select directory",
        #                                               unicode(path),
        #                                               options)
        path = Directory(path)
        directory_selector = DirectorySelector(path)
        if directory_selector.exec_():
            path = directory_selector.path
            widget = DirectoryWidget(path, self)
            widget.deleted.connect(self._delete_item)
            widget.dropped_file.connect(self.move_file)
            index = self._vertical_layout.count() -1
            self._vertical_layout.insertWidget(index, widget)
            self._widgets.append(widget)

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

####################################################################################################
# 
# End
# 
####################################################################################################
