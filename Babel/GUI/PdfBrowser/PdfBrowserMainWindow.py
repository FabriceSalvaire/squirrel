# -*- coding: utf-8 -*-

####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2014
# 
####################################################################################################

####################################################################################################

import logging

from PyQt4 import QtCore, QtGui

####################################################################################################

from .DocumentDirectory import DocumentDirectory
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
        self._document_directory = DocumentDirectory(path)
        self._path_navigator.path = path
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
                          shortcutContext=QtCore.Qt.ApplicationShortcut,
                          )

        self._next_document_action = \
            QtGui.QAction(icon_loader['arrow-right'],
                          'Next document',
                          self,
                          toolTip='Next Document',
                          triggered=self.next_document,
                          shortcut='Space',
                          shortcutContext=QtCore.Qt.ApplicationShortcut,
                          )

        self._select_action = \
            QtGui.QAction(icon_loader['get-hot-new-stuff'],
                          'Select document',
                          self,
                          toolTip='Select Document',
                          triggered=self.select_document,
                          shortcut='Ctrl+S',
                          shortcutContext=QtCore.Qt.ApplicationShortcut,
                          )

        self._fit_width_action = \
            QtGui.QAction(icon_loader['zoom-fit-width'],
                          'Fit width',
                          self,
                          toolTip='Fit width',
                          triggered=self._image_viewer.fit_width,
                          shortcut='Ctrl+W',
                          shortcutContext=QtCore.Qt.ApplicationShortcut,
                          )

        self._fit_document_action = \
            QtGui.QAction(icon_loader['zoom-fit-best'],
                          'Fit document',
                          self,
                          toolTip='Fit document',
                          triggered=self._image_viewer.fit_document,
                          shortcut='Ctrl+B',
                          shortcutContext=QtCore.Qt.ApplicationShortcut,
                          )

    ##############################################
    
    def _create_toolbar(self):

        self._page_tool_bar = self.addToolBar('Documents')
        for item in (self._previous_document_action,
                     self._next_document_action,
                     self._select_action,
                     self._fit_width_action,
                     self._fit_document_action,
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
        self._path_navigator.path_changed.connect(self.open_directory)
        self._image_viewer = ImageViewer(self)
        self._central_widget = QtGui.QWidget(self)
        self._vertical_layout = QtGui.QVBoxLayout(self._central_widget)
        self._vertical_layout.addWidget(self._path_navigator)
        self._vertical_layout.addWidget(self._image_viewer)
        self.setCentralWidget(self._central_widget)
        self.statusBar()
        self._create_actions()
        self._create_toolbar()

        self._translate_ui()

    ##############################################

    def _translate_ui(self):

        pass

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
            colour = QtGui.QColor(QtCore.Qt.white)
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
