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

"""Implement a PDF Viewer Widget.
"""

####################################################################################################
#
# * mouse
# * text selection
# * zoom selection
# * suppress margin
# * one page, facing page, etc.
# * continous mode / single page
# * full screen
# * rotate left / right
#
# * find
#
####################################################################################################

####################################################################################################
#
# Page Controller
#   - set document
#   - previous/next goto first/last page, history, corresponding widgets
#   - page changed ->
#
# Image Viewer / Controller
#   - set image provider
#   - -> page changed
#   - clear
#   - fit width/page
#
####################################################################################################

# Fixme: PDF viewer
#   - set document, in fact an image provider
#   - set page
#   - get page image according the zoom mode
#   - the image provider can use a subprocess to perform read-ahead
#   - trim margin : how to get bounding box from MuPdf ?

####################################################################################################

import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal

from Babel.Tools.EnumFactory import EnumFactory
from ..Widgets.IconLoader import IconLoader

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class ToolBar(QtWidgets.QToolBar):

    # Fixme: move

    ##############################################

    def add(self, item):

        if isinstance(item, QtWidgets.QAction):
            self.addAction(item)
        else:
            self.addWidget(item)

####################################################################################################

class PageController(QtCore.QObject):

    # Fixme: MVC ?

    page_changed = pyqtSignal(int)

    # go to first page
    # go to last page
    # previous view
    # next view

    _logger = _module_logger.getChild('PageController')

    ##############################################

    def __init__(self, document=None):

        super().__init__()

        self._application = QtWidgets.QApplication.instance()

        self._create_actions()
        self._create_toolbar()

        self.document = document

    ##############################################

    def _create_actions(self):

        icon_loader = IconLoader()

        self._previous_page_action = QtWidgets.QAction(
            icon_loader['chevron-left-black@36'],
            'Previous page',
            self._application,
            toolTip='Previous Page',
            triggered=lambda: self.previous_page(), # Fixme:
        )

        self._next_page_action = QtWidgets.QAction(
            icon_loader['chevron-right-black@36'],
            'Next page',
            self._application,
            toolTip='Next Page',
            triggered=lambda: self.next_page(),
        )

    ##############################################

    def _create_toolbar(self):

        self._page_index_line_edit = QtWidgets.QLineEdit()
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Preferred)
        self._page_index_line_edit.setSizePolicy(size_policy)
        self._last_page_index_label = QtWidgets.QLabel()

        self._tool_bar = ToolBar('Viewer')
        for item in (self._previous_page_action,
                     self._page_index_line_edit,
                     self._last_page_index_label,
                     self._next_page_action,
                     ):
            self._tool_bar.add(item)

    ##############################################

    @property
    def tool_bar(self):
        return self._tool_bar

    ##############################################

    @property
    def document(self):
        return self._document

    ##############################################

    @document.setter
    def document(self, document):

        self._document = document
        if document is None:
            self._page_index = None
            self._last_page_index_label.clear()
        else:
            self._last_page_index_label.setText('of %u' % self._document.number_of_pages)
            self.goto_page(0) # Fixme: store last page

    ##############################################

    @property
    def page_index(self):
        return self._page_index

    # @page_index.setter
    def goto_page(self, page_index):

        if (self._document is not None
            and 0 <= page_index < self._document.number_of_pages):
            self._page_index = page_index
            self._page_index_line_edit.setText(str(page_index +1))
            self.page_changed.emit(page_index)
            return True
        else:
            return False

    ##############################################

    def previous_page(self):

        self.goto_page(self._page_index -1)

    ##############################################

    def next_page(self):

        self.goto_page(self._page_index +1)

####################################################################################################

class ViewerController(QtCore.QObject):

    # Fixme: purpose, versus PageController

    zoom_mode_enum = EnumFactory('ZoomModeEnum', ('fit_document', 'fit_width'))

    # Fixme
    horizontal_margin = 40 # scroller width
    vertical_margin = 15 # widget margin?

    resolution = 1000

    _logger = _module_logger.getChild('ViewerController')

    ##############################################

    def __init__(self, document=None):

        super().__init__()

        self._application = QtWidgets.QApplication.instance()

        self._create_actions()
        self._create_toolbar()

        self._page_controller = PageController()

        self._image_widget = ImageWidget()
        self._zoom_mode = None
        self._image_cache = None

        self._page_controller.page_changed.connect(self._show_page)
        self._image_widget.resize_event.connect(self._show_page)
        self._image_widget.drag_event.connect(self._on_drag_event)

        self.document = document

    ##############################################

    @property
    def image_widget(self):
        return self._image_widget

    @property
    def tool_bar(self):
        return self._tool_bar

    @property
    def page_controller(self):
        return self._page_controller

    ##############################################

    def _create_actions(self):

        icon_loader = IconLoader()

        self._fit_width_action = QtWidgets.QAction(
            icon_loader['zoom-fit-width@36'],
            'Fit width',
            self._application,
            toolTip='Fit width',
            triggered=self.fit_width,
            shortcut='Ctrl+W',
            shortcutContext=Qt.ApplicationShortcut,
        )

        self._fit_document_action = QtWidgets.QAction(
            icon_loader['settings-overscan-black@36'], # zoom-fit-best
            'Fit document',
            self._application,
            toolTip='Fit document',
            triggered=self.fit_document,
            shortcut='Ctrl+B',
            shortcutContext=Qt.ApplicationShortcut,
        )

    ##############################################

    def _create_toolbar(self):

        self._tool_bar = ToolBar('Viewer')
        for item in (
                self._fit_width_action,
                self._fit_document_action,
        ):
            self._tool_bar.add(item)

    ##############################################

    @property
    def document(self):
        return self._document

    ##############################################

    @document.setter
    def document(self, document):

        self._document = document
        self._page_controller.document = document # emit page_changed
        if document is None:
            self._zoom_mode = None
            self._image_cache = None
            self._image_widget.clear()
        else:
            self._image_cache = document.image_cache
            self.fit_document() # recall _show_page

    ##############################################

    def fit_width(self):

        self._logger.info('')
        # Fixme: resolution versus dimension
        self._zoom_mode = self.zoom_mode_enum.fit_width
        # Fixme: update page
        image_widget = self._image_widget
        image = self._image_cache.to_pixmap(
            self._page_controller.page_index,
            width=image_widget.width() -self.horizontal_margin,
            height=0,
            resolution=1000,
        )
        image_widget.set_pixmap(image)

    ##############################################

    def fit_document(self):

        image_widget = self._image_widget
        self._logger.info('widget size: %ux%u', image_widget.width(), image_widget.height())
        self._zoom_mode = self.zoom_mode_enum.fit_document
        image = self._image_cache.to_pixmap(
            self._page_controller.page_index,
            width=image_widget.width() -self.horizontal_margin,
            height=image_widget.height() -self.vertical_margin,
            resolution=1000,
        )
        image_widget.set_pixmap(image)

    ##############################################

    def _show_page(self):

        self._logger.info("page %u", self._page_controller.page_index)

        if self._zoom_mode is not None:
            if self._zoom_mode == self.zoom_mode_enum.fit_document:
                self.fit_document()
            elif self._zoom_mode == self.zoom_mode_enum.fit_width:
                self.fit_width()

    ##############################################

    def _on_drag_event(self):

        if self._document is not None:
            document = self._document
            drag = QtGui.QDrag(self)
            mime_data = QtCore.QMimeData()
            document_path = str(document.path)
            url = QtCore.QUrl.fromLocalFile(document_path)
            mime_data.setUrls((url,))
            drag.setMimeData(mime_data)
            icon_loader = IconLoader()
            drag.setPixmap(icon_loader['application-pdf'].pixmap(32, 32))
            drop_action = drag.exec_()

####################################################################################################

class ImageWidget(QtWidgets.QScrollArea):

    resize_event = pyqtSignal()
    drag_event = pyqtSignal()

    _logger = _module_logger.getChild('ImageWidget')

    ##############################################

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWidgetResizable(True)
        self._pixmap_label = QtWidgets.QLabel()
        self._pixmap_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setWidget(self._pixmap_label)
        self._empty = True

    ##############################################

    def clear(self):

        self._pixmap_label.clear()
        self._empty = True

    ##############################################

    def set_pixmap(self, image):

        # self.update_style()
        height, width = image.shape[:2]
        qimage = QtGui.QImage(image.data, width, height, QtGui.QImage.Format_ARGB32)
        self._pixmap_label.setPixmap(QtGui.QPixmap.fromImage(qimage))
        self._empty = False

    ##############################################

    def resizeEvent(self, event):

        self._logger.info("")
        self.resize_event.emit()

    ##############################################

    def mousePressEvent(self, event):

        if not self._empty and event.button() == Qt.LeftButton:
            self.drag_event.emit()

    ##############################################

    # def update_style(self):

    #     # Fixme: move to sub-class

    #     if self._document.selected:
    #         margin = 15
    #         colour = QtGui.QColor()
    #         colour.setHsv(210, 150, 250)
    #     else:
    #         margin = 0
    #         colour = QtGui.QColor(Qt.white)
    #     self._pixmap_label.setStyleSheet("border: {}px solid {};".format(margin, colour.name()))
