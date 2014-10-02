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

from PyQt4 import QtCore, QtGui

####################################################################################################

from Babel.GUI.Widgets.RowLayoutManager import RowLayoutManager

####################################################################################################

class InfoPage(QtGui.QWidget):

    ##############################################

    def __init__(self, main_window):

        super(InfoPage, self).__init__()
        
        self._main_window = main_window
        self._init_ui()

    ##############################################

    def _init_ui(self):

        self._widgets = {}

        vertical_layout = QtGui.QVBoxLayout(self)

        grid_layout = QtGui.QGridLayout()
        row_layout_manager = RowLayoutManager(grid_layout)
        vertical_layout.addLayout(grid_layout)
        application = QtGui.QApplication.instance()
        palette = QtGui.QPalette(application.palette())
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        for key, title in (
            ('path', u'Path'),
            ('number_of_pages', u'Number of pages'),
            ('Title', u'Title'),
            ('Subject', u'Subject'),
            ('Author', u'Author'),
            ('Creator', u'Creator'),
            ('Producer', u'Producer'),
            ('CreationDate', u'Creation Date'),
            ('ModDate', u'Modification Date'),
            ):
            label = QtGui.QLabel(self)
            label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
            label.setText(title + u':')
            line_edit = QtGui.QLineEdit(self)
            self._widgets[key] = line_edit
            # line_edit.setPalette(palette)
            # line_edit.setFrame(False)
            line_edit.setReadOnly(True)
            label.setBuddy(line_edit)
            row_layout_manager.add_row((label, line_edit))

        label = QtGui.QLabel(self)
        label.setText(u'XML Metadata:')
        self._text_browser = QtGui.QTextBrowser(self)
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self._text_browser.setSizePolicy(size_policy)
        label.setBuddy(self._text_browser)
        vertical_layout.addWidget(label)
        vertical_layout.addWidget(self._text_browser)

        # spacer_item = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        # vertical_layout.addItem(spacer_item)

    ##############################################

    def open_pdf(self):

        pdf_document = self._main_window._pdf_document
        pdf_metadata = pdf_document.metadata
        key_value_pairs = [('path', unicode(pdf_document.path)),
                           ('number_of_pages', str(pdf_document.number_of_pages)),
                           ]
        for key in ('Title', 'Subject', 'Author', 'Creator', 'Producer', 'CreationDate', 'ModDate'):
            key_value_pairs.append((key, pdf_metadata[key] or ''))
        for key, value in key_value_pairs:
            self._widgets[key].setText(value)
        self._text_browser.setPlainText(pdf_metadata.metadata or '')
            
####################################################################################################
#
# End
#
####################################################################################################
