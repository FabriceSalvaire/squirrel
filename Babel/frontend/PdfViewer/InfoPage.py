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

from PyQt5 import QtCore, QtGui, QtWidgets

####################################################################################################

from ..Widgets.RowLayoutManager import RowLayoutManager

####################################################################################################

class InfoPage(QtWidgets.QWidget):

    ##############################################

    def __init__(self, main_window):

        super(InfoPage, self).__init__()

        self._main_window = main_window
        self._init_ui()

    ##############################################

    def _init_ui(self):

        self._widgets = {}

        vertical_layout = QtWidgets.QVBoxLayout(self)

        grid_layout = QtWidgets.QGridLayout()
        row_layout_manager = RowLayoutManager(grid_layout)
        vertical_layout.addLayout(grid_layout)
        application = QtWidgets.QApplication.instance()
        palette = QtGui.QPalette(application.palette())
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        for key, title in (
            ('path', 'Path'),
            ('number_of_pages', 'Number of pages'),
            ('Title', 'Title'),
            ('Subject', 'Subject'),
            ('Author', 'Author'),
            ('Creator', 'Creator'),
            ('Producer', 'Producer'),
            ('CreationDate', 'Creation Date'),
            ('ModDate', 'Modification Date'),
            ):
            label = QtWidgets.QLabel(self)
            label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
            label.setText(title + ':')
            line_edit = QtWidgets.QLineEdit(self)
            self._widgets[key] = line_edit
            # line_edit.setPalette(palette)
            # line_edit.setFrame(False)
            line_edit.setReadOnly(True)
            label.setBuddy(line_edit)
            row_layout_manager.add_row((label, line_edit))

        label = QtWidgets.QLabel(self)
        label.setText('XML Metadata:')
        self._text_browser = QtWidgets.QTextBrowser(self)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self._text_browser.setSizePolicy(size_policy)
        label.setBuddy(self._text_browser)
        vertical_layout.addWidget(label)
        vertical_layout.addWidget(self._text_browser)

        # spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # vertical_layout.addItem(spacer_item)

    ##############################################

    def open_pdf(self):

        # QML: pass a QmlPdfDocument
        #   requires properties

        pdf_document = self._main_window._pdf_document
        pdf_metadata = pdf_document.metadata
        key_value_pairs = [
            ('path', str(pdf_document.path)),
            ('number_of_pages', str(pdf_document.number_of_pages)),
        ]
        for key in ('Title', 'Subject', 'Author', 'Creator', 'Producer', 'CreationDate', 'ModDate'):
            key_value_pairs.append((key, pdf_metadata[key] or ''))
        for key, value in key_value_pairs:
            self._widgets[key].setText(value)
        self._text_browser.setPlainText(pdf_metadata.metadata or '')
