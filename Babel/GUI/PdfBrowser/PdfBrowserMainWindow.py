# -*- coding: utf-8 -*-

####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2014
# 
####################################################################################################

####################################################################################################

from PyQt4 import QtCore, QtGui

####################################################################################################

from .DocumentDirectory import DocumentDirectory
from Babel.GUI.MainWindowBase import MainWindowBase
from Babel.GUI.Widgets.IconLoader import IconLoader

####################################################################################################

class PdfBrowserMainWindow(MainWindowBase):

    ##############################################

    def __init__(self, path=None, parent=None):

        super(PdfBrowserMainWindow, self).__init__(title='Babel PDF Browser', parent=parent)

        self._init_ui()
        if path is not None:
            self.open_directory(path)

    ##############################################

    def open_directory(self, path):

        self._document_directory = DocumentDirectory(path)
        self._show_document()

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
        self._image_viewer.update_style(document)

    ##############################################
    
    def _create_actions(self):

        icon_loader = IconLoader()

        self._previous_document_action = \
            QtGui.QAction(icon_loader['arrow-left'],
                          'Previous document',
                          self,
                          toolTip='Previous Document',
                          triggered=lambda: self.previous_document(),
                          shortcut='Backspace',
                          shortcutContext=QtCore.Qt.ApplicationShortcut,
                          )

        self._next_document_action = \
            QtGui.QAction(icon_loader['arrow-right'],
                          'Next document',
                          self,
                          toolTip='Next Document',
                          triggered=lambda: self.next_document(),
                          shortcut='Space',
                          shortcutContext=QtCore.Qt.ApplicationShortcut,
                          )

        self._select_action = \
            QtGui.QAction(icon_loader['get-hot-new-stuff'],
                          'Select document',
                          self,
                          toolTip='Select Document',
                          triggered=lambda: self.select_document(),
                          shortcut='Ctrl+S',
                          shortcutContext=QtCore.Qt.ApplicationShortcut,
                          )

    ##############################################
    
    def _create_toolbar(self):

        self._page_tool_bar = self.addToolBar('Documents')
        for item in (self._previous_document_action,
                     self._next_document_action,
                     self._select_action,
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

        self._image_viewer = ImageViewer(self)
        self.setCentralWidget(self._image_viewer)
        self.statusBar()
        self._create_actions()
        self._create_toolbar()

        self._translate_ui()

    ##############################################

    def _translate_ui(self):

        pass

####################################################################################################

class ImageViewer(QtGui.QScrollArea):

    ##############################################

    def __init__(self, main_window):

        super(ImageViewer, self).__init__()

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

    def update(self, document):

        self.update_style(document)

        image = document.image
        height, width = image.shape[:2]
        qimage = QtGui.QImage(image.data, width, height, QtGui.QImage.Format_ARGB32)
        self._pixmap_label.setPixmap(QtGui.QPixmap.fromImage(qimage))

    ##############################################

    def update_style(self, document):

        if document.selected:
            margin = 15
            colour = QtGui.QColor()
            colour.setHsv(210, 150, 250)
        else:
            margin = 0
            colour = QtGui.QColor(QtCore.Qt.white)
        self._pixmap_label.setStyleSheet("border: {}px solid {};".format(margin, colour.name()))
            
####################################################################################################
#
# End
#
####################################################################################################
