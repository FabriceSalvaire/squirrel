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

from Babel.GUI.MainWindowBase import MainWindowBase

####################################################################################################

class MainWindow(MainWindowBase):

    ##############################################

    def __init__(self):

        super(MainWindow, self).__init__(title='Babel')

        self._init_ui()

    ##############################################

    def init_menu(self):

        super(MainWindow, self).init_menu()

        self._file_menu.addAction(self._application.open_files_action)

    ##############################################

    def _init_ui(self):

        self.statusBar()

        self.splitter = QtGui.QSplitter(self)
        self.setCentralWidget(self.splitter)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)

        self.library_tree_view = QtGui.QTreeView(self)
        self.splitter.addWidget(self.library_tree_view)

        self.library_table_view = QtGui.QTableView(self)
        self.splitter.addWidget(self.library_table_view)

        self.item_tab_widget = QtGui.QTabWidget(self)
        self.splitter.addWidget(self.item_tab_widget)

        self._init_details_tab()
        self._init_notes_tab()
        self.item_tab_widget.setCurrentIndex(self.item_tab_widget.indexOf(self.details_tab))

        self._translate_ui()

    ##############################################

    def _init_details_tab(self):

        self.details_tab = QtGui.QWidget()
        self.item_tab_widget.addTab(self.details_tab, "")
        vertical_layout = QtGui.QVBoxLayout(self.details_tab)

        self.type_label = QtGui.QLabel(self.details_tab)
        self.type_combo_box = QtGui.QComboBox(self.details_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.type_combo_box.sizePolicy().hasHeightForWidth())
        self.type_combo_box.setSizePolicy(sizePolicy)
        self.type_label.setBuddy(self.type_combo_box)
        horizontal_layout = QtGui.QHBoxLayout()
        horizontal_layout.addWidget(self.type_label)
        horizontal_layout.addWidget(self.type_combo_box)
        vertical_layout.addLayout(horizontal_layout)

        self.title_line_edit = QtGui.QLineEdit(self.details_tab)
        vertical_layout.addWidget(self.title_line_edit)

        self.authors_label = QtGui.QLabel(self.details_tab)
        self.authors_line_edit = QtGui.QLineEdit(self.details_tab)
        self.authors_label.setBuddy(self.authors_line_edit)
        horizontal_layout = QtGui.QHBoxLayout()
        horizontal_layout.addWidget(self.authors_label)
        horizontal_layout.addWidget(self.authors_line_edit)
        vertical_layout.addLayout(horizontal_layout)

        spacer_item = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        vertical_layout.addItem(spacer_item)

    ##############################################

    def _init_notes_tab(self):

        self.notes_tab = QtGui.QWidget()
        self.item_tab_widget.addTab(self.notes_tab, "")
        vertical_layout = QtGui.QVBoxLayout(self.notes_tab)

        self.notes_label = QtGui.QLabel(self.notes_tab)
        self.notes_text_edit = QtGui.QTextEdit(self.notes_tab)
        vertical_layout.addWidget(self.notes_label)
        vertical_layout.addWidget(self.notes_text_edit)

        spacer_item = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        vertical_layout.addItem(spacer_item)

    ##############################################

    def _translate_ui(self):

        self.item_tab_widget.setTabText(self.item_tab_widget.indexOf(self.details_tab),
                                        self.translate("Details"))
        self.type_label.setText(self.translate("Type:"))
        self.authors_label.setText(self.translate("Authors:"))

        self.item_tab_widget.setTabText(self.item_tab_widget.indexOf(self.notes_tab),
                                        self.translate("Notes"))
        self.notes_label.setText(self.translate("Notes:"))

    ##############################################

    def closeEvent(self, event=None):

        self._application.exit()

####################################################################################################
#
# End
#
####################################################################################################
