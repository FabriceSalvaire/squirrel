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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

####################################################################################################

from .DirectoryListWidget import DirectoryListWidget
from .DirectoryTocWidget import DirectoryTocWidget
from .DocumentDirectory import DocumentDirectory
from Babel.FileSystem.DirectoryToc import DirectoryToc
from Babel.GUI.MainWindowBase import MainWindowBase
from Babel.GUI.Widgets.IconLoader import IconLoader
from Babel.GUI.Widgets.PathNavigator import PathNavigator

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class PdfBrowserMainWindow(MainWindowBase):

    _logger = _module_logger.getChild('PdfBrowserMainWindow')

    ##############################################

    def __init__(self, parent=None):

        super(PdfBrowserMainWindow, self).__init__(title='Babel PDF Browser', parent=parent)

        self._init_ui()

    ##############################################

    def open_directory(self, path):

        # Fixme: move to application?
        self._directory_toc.update(DirectoryToc(path))
        self._path_navigator.set_path(path) # Fixme: path_navigator -> open_directory -> path_navigator
        self._document_directory = DocumentDirectory(path)
        if self._document_directory:
            self._show_document()
        else:
            self._image_viewer.clear()

    ##############################################

    def previous_document(self):

        try:
            self._document_directory.previous()
            self._show_document()
        except StopIteration:
            pass

    ##############################################

    def next_document(self):

        try:
            self._document_directory.next()
            self._show_document()
        except StopIteration:
            pass

    ##############################################

    def current_document(self):

        return self._document_directory.current_item

    ##############################################

    def _show_document(self):

        self._image_viewer.update(self.current_document())

    ##############################################

    def select_document(self):

        document = self.current_document()
        document.selected = not document.selected
        self._image_viewer.update_style()

    ##############################################
    
    def _create_actions(self):

        icon_loader = IconLoader()

        self._previous_document_action = \
            QtGui.QAction(icon_loader['arrow-left'],
                          'Previous document',
                          self,
                          toolTip='Previous Document',
                          triggered=self.previous_document,
                          shortcut='Backspace',
                          shortcutContext=Qt.ApplicationShortcut,
                          )

        self._next_document_action = \
            QtGui.QAction(icon_loader['arrow-right'],
                          'Next document',
                          self,
                          toolTip='Next Document',
                          triggered=self.next_document,
                          shortcut='Space',
                          shortcutContext=Qt.ApplicationShortcut,
                          )

        self._select_action = \
            QtGui.QAction(icon_loader['get-hot-new-stuff'],
                          'Select document',
                          self,
                          toolTip='Select Document',
                          triggered=self.select_document,
                          shortcut='Ctrl+S',
                          shortcutContext=Qt.ApplicationShortcut,
                          )

        self._fit_width_action = \
            QtGui.QAction(icon_loader['zoom-fit-width'],
                          'Fit width',
                          self,
                          toolTip='Fit width',
                          triggered=self._image_viewer.fit_width,
                          shortcut='Ctrl+W',
                          shortcutContext=Qt.ApplicationShortcut,
                          )

        self._fit_document_action = \
            QtGui.QAction(icon_loader['zoom-fit-best'],
                          'Fit document',
                          self,
                          toolTip='Fit document',
                          triggered=self._image_viewer.fit_document,
                          shortcut='Ctrl+B',
                          shortcutContext=Qt.ApplicationShortcut,
                          )

        self._pdf_browser_mode_action = \
            QtGui.QAction(icon_loader['application-pdf'],
                          'PDF browser mode',
                          self,
                          toolTip='PDF browser mode',
                          triggered=self._pdf_browser_mode,
                          shortcut='Ctrl+P',
                          shortcutContext=Qt.ApplicationShortcut,
                          )

        self._directory_toc_mode_action = \
            QtGui.QAction(icon_loader['folder-blue'],
                          'Directory toc mode',
                          self,
                          toolTip='Directory toc mode',
                          triggered=self._directory_toc_mode,
                          shortcut='Ctrl+D',
                          shortcutContext=Qt.ApplicationShortcut,
                          )

    ##############################################
    
    def _create_toolbar(self):

        self._page_tool_bar = self.addToolBar('Documents')
        for item in (self._previous_document_action,
                     self._next_document_action,
                     self._select_action,
                     self._fit_width_action,
                     self._fit_document_action,
                     self._directory_toc_mode_action,
                     self._pdf_browser_mode_action,
                    ):
            if isinstance(item,QtGui.QAction):
                self._page_tool_bar.addAction(item)
            else:
                self._page_tool_bar.addWidget(item)

    ##############################################

    def init_menu(self):

        super(PdfBrowserMainWindow, self).init_menu()

    ##############################################

    def _init_ui(self):

        self._path_navigator = PathNavigator(self)
        self._directory_toc = DirectoryTocWidget()
        self._path_navigator.path_changed.connect(self.open_directory)
        self._directory_toc.path_changed.connect(self.open_directory)
        self._image_viewer = ImageViewer(self)
        self._image_viewer.hide()
        self._central_widget = QtGui.QWidget(self)
        self._vertical_layout = QtGui.QVBoxLayout(self._central_widget)
        self._vertical_layout.addWidget(self._path_navigator)
        self._vertical_layout.addWidget(self._directory_toc)
        self._vertical_layout.addWidget(self._image_viewer)
        self.setCentralWidget(self._central_widget)
        self.statusBar()
        self._create_actions()
        self._create_toolbar()

        self._directory_list_dock_widget = QtGui.QDockWidget(self)
        self._directory_list_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self._directory_list = DirectoryListWidget(self)
        self._directory_list_dock_widget.setWidget(self._directory_list)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._directory_list_dock_widget)

        self._translate_ui()

    ##############################################

    def _translate_ui(self):

        pass

    ##############################################

    def _directory_toc_mode(self):

        self._directory_toc.show()
        self._image_viewer.hide()

    ##############################################

    def _pdf_browser_mode(self):

        self._directory_toc.hide()
        self._image_viewer.show()

    ##############################################

    def mousePressEvent(self, event):

        if (event.button() == Qt.LeftButton and
            self._image_viewer.geometry().contains(event.pos())):

            drag = QtGui.QDrag(self)
            mime_data = QtCore.QMimeData()
            document_path = str(self.current_document().path)
            url = QtCore.QUrl.fromLocalFile(document_path)
            mime_data.setUrls((url,))
            drag.setMimeData(mime_data)
            icon_loader = IconLoader()
            drag.setPixmap(icon_loader['application-pdf'].pixmap(32, 32))

            drop_action = drag.exec_()
        
####################################################################################################

class ImageViewer(QtGui.QScrollArea):

    _logger = _module_logger.getChild('ImageViewer')

    ##############################################

    def __init__(self, main_window):

        super(ImageViewer, self).__init__()

        self._main_window = main_window
        self._init_ui()

        self._document = None

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

        # self._logger.info('')
        # Fixme: resolution versus dimension
        image = self._document.load(width=self.width(), height=0, resolution=1000)
        self._set_pixmap(image)

    ##############################################

    def fit_document(self):

        # self._logger.info('')
        image = self._document.load(width=self.width(), height=self.height(), resolution=1000)
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
            
####################################################################################################
#
# End
#
####################################################################################################
