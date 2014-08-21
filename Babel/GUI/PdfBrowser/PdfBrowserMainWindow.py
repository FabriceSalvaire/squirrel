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

from Babel.FileSystem.File import Path, Directory
from Babel.GUI.MainWindowBase import MainWindowBase
from Babel.GUI.Widgets.IconLoader import IconLoader
from Babel.Pdf.PdfDocument import PdfDocument

####################################################################################################

class PdfBrowserMainWindow(MainWindowBase):

    importable_mime_types = ('application/pdf',
                             )

    ##############################################

    def __init__(self, path=None, parent=None):

        super(PdfBrowserMainWindow, self).__init__(title='Babel PDF Browser', parent=parent)

        self._init_ui()
        if path is not None:
            self.open_directory(Directory(path))

    ##############################################

    def _is_file_importable(self, file_path):

        return file_path.mime_type in self.importable_mime_types

    ##############################################

    def open_directory(self, path):

        self._file_paths = [file_path
                            for file_path in path.iter_file()
                            if self._is_file_importable(file_path)]
        # implement a ring or linked list
        self._file_index = 0
        self.open_document()

    ##############################################

    def current_document(self):

        return self._file_paths[self._file_index]

    ##############################################

    def open_document(self):

        path = self.current_document()

        self._pdf_document = PdfDocument(path)
        self._pdf_page = self._pdf_document[0]
        self._image_viewer.update_page(self._pdf_page)

    ##############################################

    def previous_document(self):

        if self._file_index > 0:
            self._file_index -= 1
            self.open_document()

    ##############################################

    def next_document(self):

        if self._file_index < len(self._file_paths) -1:
            self._file_index += 1
            self.open_document()

    ##############################################
    
    def _create_actions(self):

        icon_loader = IconLoader()

        self._previous_document_action = \
            QtGui.QAction(icon_loader['arrow-left'],
                          'Previous document',
                          self,
                          toolTip='Previous Document',
                          triggered=lambda: self.previous_document(),
                          )

        self._next_document_action = \
            QtGui.QAction(icon_loader['arrow-right'],
                          'Next document',
                          self,
                          toolTip='Next Document',
                          triggered=lambda: self.next_document(),
                          )

    ##############################################
    
    def _create_toolbar(self):

        self._page_tool_bar = self.addToolBar('Documents')
        for item in (self._previous_document_action,
                     self._next_document_action,
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

    def update_page(self, pdf_page):

        np_array = pdf_page.to_pixmap(resolution=150)
        height, width = np_array.shape[:2]
        image = QtGui.QImage(np_array.data, width, height, QtGui.QImage.Format_ARGB32)
        self._pixmap_label.setPixmap(QtGui.QPixmap.fromImage(image))
            
####################################################################################################
#
# End
#
####################################################################################################
