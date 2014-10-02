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

from PyQt4 import QtCore, QtGui

####################################################################################################

from Babel.GUI.Widgets.GrowingTextBrowser import GrowingTextBrowser

####################################################################################################

class TextPage(QtGui.QScrollArea):

    ##############################################

    def __init__(self, main_window):

        super(TextPage, self).__init__()
        
        self._main_window = main_window
        self._init_ui()

    ##############################################

    def _init_ui(self):

        # self._scroll_area = QtGui.QScrollArea(self)
        # self._scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

        self._container_widget = QtGui.QWidget()
        self._vertical_layout = QtGui.QVBoxLayout(self._container_widget) # Set container_widget layout
        self._spacer_item = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
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

    def update_page(self):

        self._clear_layout()
        pdf_page = self._main_window._pdf_page
        text_page = pdf_page.to_text()
        with codecs.open('log%u.txt' % pdf_page.page_number,
                         encoding='utf-8', mode='w+') as log_file:
            log_file.write(text_page.dump_text_page_xml(dump_char=True))
        for text_block in sorted(text_page.blocks):
            self._append_block(text_block)
        self._vertical_layout.addItem(self._spacer_item)

    ##############################################
            
    def _append_block(self, block_text):

        horizontal_layout = QtGui.QHBoxLayout()
        combo_box = QtGui.QComboBox() # self._container_widget
        for item in ('Text', 'Title', 'Authors', 'Abstract', 'Refrences'):
            combo_box.addItem(item)
        text_browser = GrowingTextBrowser() # self._container_widget
        text_browser.setPlainText(unicode(block_text))
        horizontal_layout.addWidget(combo_box, 0, QtCore.Qt.AlignTop)
        horizontal_layout.addWidget(text_browser, 0, QtCore.Qt.AlignTop)
        self._vertical_layout.addLayout(horizontal_layout)
            
####################################################################################################
#
# End
#
####################################################################################################
