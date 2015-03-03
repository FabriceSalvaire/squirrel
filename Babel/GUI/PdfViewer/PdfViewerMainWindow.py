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

import codecs

from PyQt5 import QtCore, QtWidgets

####################################################################################################

from .ImagePage import ImagePage
from .InfoPage import InfoPage
from .TextPage import TextPage
from Babel.GUI.Base.MainWindowBase import MainWindowBase
from Babel.GUI.Widgets.IconLoader import IconLoader
from Babel.Pdf.PdfDocument import PdfDocument

####################################################################################################

class PdfViewerMainWindow(MainWindowBase):

    ##############################################

    def __init__(self, pdf_path=None, parent=None):

        super(PdfViewerMainWindow, self).__init__(title='Babel PDF Viewer', parent=parent)

        self._init_ui()
        if pdf_path is not None:
            self.open_pdf(pdf_path)

    ##############################################

    def open_pdf(self, path):

        self._pdf_document = PdfDocument(path)
        self._info_page.open_pdf()
        self._last_page_number_label.setText('of %u' % self._pdf_document.number_of_pages)
        self._set_page_number(0)
        # Fixme: page cache, speed-up

    ##############################################

    def _set_page_number(self, page_number):

        if 0 <= page_number < self._pdf_document.number_of_pages:
            self._page_number_line_edit.setText(str(page_number +1))
            self._pdf_page = self._pdf_document[page_number]
            for page in (self._image_page,
                         self._text_page,
                         ):
                page.update_page()

    ##############################################

    def previous_page(self):

        self._set_page_number(self._pdf_page.page_number -1)

    ##############################################

    def next_page(self):

        self._set_page_number(self._pdf_page.page_number +1)

    ##############################################
    
    def _create_actions(self):

        icon_loader = IconLoader()

        self._show_info_action = \
            QtWidgets.QAction('Info',
                          self,
                          toolTip='Info',
                          checkable=True,
                          triggered=lambda: self._set_current_widget(self._info_page),
                          )

        self._show_image_action = \
            QtWidgets.QAction('Image',
                          self,
                          toolTip='Image',
                          checkable=True,
                          triggered=lambda: self._set_current_widget(self._image_page),
                          )

        self._show_text_action = \
            QtWidgets.QAction('Text',
                          self,
                          toolTip='Text',
                          checkable=True,
                          triggered=lambda: self._set_current_widget(self._text_page),
                          )

        self._action_group = QtWidgets.QActionGroup(self)
        for action in (self._show_info_action,
                       self._show_image_action,
                       self._show_text_action,
                       ):
            self._action_group.addAction(action)

        self._previous_page_action = \
            QtWidgets.QAction(icon_loader['arrow-left'],
                          'Previous page',
                          self,
                          toolTip='Previous Page',
                          triggered=lambda: self.previous_page(),
                          )

        self._next_page_action = \
            QtWidgets.QAction(icon_loader['arrow-right'],
                          'Next page',
                          self,
                          toolTip='Next Page',
                          triggered=lambda: self.next_page(),
                          )

    ##############################################
    
    def _create_toolbar(self):

        self._show_info_action.setChecked(True)
        self._mode_tool_bar = self.addToolBar('Mode')
        for action in (self._show_info_action,
                       self._show_image_action,
                       self._show_text_action,
                       ):
            self._mode_tool_bar.addAction(action)

        self._page_number_line_edit = QtWidgets.QLineEdit()
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self._page_number_line_edit.setSizePolicy(size_policy)
        self._last_page_number_label = QtWidgets.QLabel()

        self._page_tool_bar = self.addToolBar('Pages')
        for item in (self._previous_page_action,
                     self._page_number_line_edit,
                     self._last_page_number_label,
                     self._next_page_action,
                     ):
            if isinstance(item,QtWidgets.QAction):
                self._page_tool_bar.addAction(item)
            else:
                self._page_tool_bar.addWidget(item)

    ##############################################

    def init_menu(self):

        super(PdfViewerMainWindow, self).init_menu()

    ##############################################

    def _init_ui(self):

        self._stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self._stacked_widget)
        self._info_page = InfoPage(self)
        self._image_page = ImagePage(self)
        self._text_page = TextPage(self)
        for page in (self._info_page,
                     self._image_page,
                     self._text_page,
                     ):
            self._stacked_widget.addWidget(page)
        self.statusBar()
        self._create_actions()
        self._create_toolbar()

        self._translate_ui()

    ##############################################

    def _translate_ui(self):

        pass

    ##############################################

    def _set_current_widget(self, widget):

        self._stacked_widget.setCurrentWidget(widget)

####################################################################################################
#
# End
#
####################################################################################################
