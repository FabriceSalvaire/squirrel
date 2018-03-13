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

from Babel.GUI.Widgets.GrowingTextBrowser import GrowingTextBrowser

####################################################################################################

class TextPage(QtWidgets.QScrollArea):

    ##############################################

    def __init__(self, main_window):

        super(TextPage, self).__init__()

        self._main_window = main_window
        self._init_ui()

    ##############################################

    def _init_ui(self):

        # self._scroll_area = QtWidgets.QScrollArea(self)
        # self._scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

        self._container_widget = QtWidgets.QWidget()
        self._vertical_layout = QtWidgets.QVBoxLayout(self._container_widget) # Set container_widget layout
        self._spacer_item = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.setWidget(self._container_widget)

    ##############################################

    def _clear_layout(self):

        layout = self._vertical_layout
        while layout.count():
            sub_layout = layout.takeAt(0).layout()
            if sub_layout is not None: # else it is the spacer_item
                while sub_layout.count():
                    widget = sub_layout.takeAt(0).widget()
                    widget.deleteLater()

    ##############################################

    def on_page_changed(self, page_index):

        # QML: pass a QmlPdfDocument
        #  require an iterator blocks -> string

        self._clear_layout()
        pdf_page = self._main_window._pdf_document[page_index]
        text_page = pdf_page.text
        for text_block in sorted(text_page.blocks):
            self._append_block(text_block)
        self._vertical_layout.addItem(self._spacer_item)

    ##############################################

    def _append_block(self, block_text):

        horizontal_layout = QtWidgets.QHBoxLayout()
        combo_box = QtWidgets.QComboBox() # self._container_widget
        for item in ('Text', 'Title', 'Authors', 'Abstract', 'Refrences'):
            combo_box.addItem(item)
        text_browser = GrowingTextBrowser() # self._container_widget
        text_browser.setPlainText(str(block_text))
        horizontal_layout.addWidget(combo_box, 0, QtCore.Qt.AlignTop)
        horizontal_layout.addWidget(text_browser, 0, QtCore.Qt.AlignTop)
        self._vertical_layout.addLayout(horizontal_layout)
