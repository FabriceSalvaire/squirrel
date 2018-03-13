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

####################################################################################################

from PyQt5 import QtCore, QtWidgets

####################################################################################################

from Babel.GUI.Base.MainWindowBase import MainWindowBase
from Babel.GUI.PdfBrowser.PdfViewer import ViewerController
from Babel.GUI.Widgets.IconLoader import IconLoader
from Babel.Pdf.PdfDocument import PdfDocument
from .InfoPage import InfoPage
from .TextPage import TextPage

####################################################################################################

class PdfViewerMainWindow(MainWindowBase):

    ##############################################

    def __init__(self, pdf_path=None, parent=None):

        super().__init__(title='Babel PDF Viewer', parent=parent)

        self._init_ui()
        if pdf_path is not None:
            self.open_pdf(pdf_path)

    ##############################################

    def open_pdf(self, path):

        self._pdf_document = PdfDocument(path)
        self._info_page.open_pdf()
        self._viewer_controller.document = self._pdf_document

    ##############################################

    def _create_actions(self):

        icon_loader = IconLoader()

        self._show_info_action =  QtWidgets.QAction(
            icon_loader['description-black@36'],
            'Info',
            self,
            toolTip='Info',
            checkable=True,
            triggered=lambda: self._set_current_widget(self._info_page),
        )

        self._show_image_action = QtWidgets.QAction(
            icon_loader['image-black@36'],
            'Image',
            self,
            toolTip='Image',
            checkable=True,
            triggered=lambda: self._set_current_widget(self._image_page),
        )

        self._show_text_action = QtWidgets.QAction(
            icon_loader['title-black@36'],
            'Text',
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

    ##############################################

    def _create_toolbar(self):

        self._show_info_action.setChecked(True)
        self._mode_tool_bar = self.addToolBar('Mode')
        for action in (self._show_info_action,
                       self._show_image_action,
                       self._show_text_action,
                       ):
            self._mode_tool_bar.addAction(action)

        self.addToolBar(self._viewer_controller.tool_bar)
        self.addToolBar(self._viewer_controller.page_controller.tool_bar)

    ##############################################

    def init_menu(self):
        super(PdfViewerMainWindow, self).init_menu()

    ##############################################

    def _init_ui(self):

        self._viewer_controller = ViewerController()

        self._stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self._stacked_widget)
        self._info_page = InfoPage(self)
        self._image_page = self._viewer_controller.image_widget
        self._text_page = TextPage(self)
        for page in (
                self._info_page,
                self._image_page,
                self._text_page,
        ):
            self._stacked_widget.addWidget(page)
        self.statusBar()
        self._create_actions()
        self._create_toolbar()

        self._viewer_controller.page_controller.page_changed.connect(self._text_page.on_page_changed)

    ##############################################

    def _set_current_widget(self, widget):
        self._stacked_widget.setCurrentWidget(widget)
