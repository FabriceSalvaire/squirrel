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

import logging
import os
import subprocess

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtQuickWidgets import QQuickWidget

from Babel.Config import ConfigInstall
from Babel.Document.DocumentDirectory import DocumentDirectory
from Babel.FileSystem.AutomaticFileRename import AutomaticFileRename
from Babel.FileSystem.File import Directory, File
from Babel.Tools.Container import EmptyRingError
from ..Base.MainWindowBase import MainWindowBase
from ..Widgets.IconLoader import IconLoader
from ..Widgets.MessageBox import MessageBox
from ..Widgets.PathNavigator import PathNavigator
from .DirectoryListWidget import DirectoryListWidget
from .DirectoryToc import DirectoryToc
from .DirectoryTocWidget import DirectoryTocWidget
from .PdfViewer import ViewerController

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class PdfBrowserMainWindow(MainWindowBase):

    _logger = _module_logger.getChild('PdfBrowserMainWindow')

    HORIZONTAL_DOCK_AREA = Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea

    ##############################################

    def __init__(self, parent=None):

        super().__init__(title='Babel PDF Browser', parent=parent)

        self._current_path = None

        self._init_ui()

    ##############################################

    @property
    def qml_engine(self):
        return self._application.qml_engine

    ##############################################

    def _tr(self, text):

        # Fixme: translate
        self._application.translate('main_window', text)

    ##############################################

    def _init_ui(self):

        self._central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self._central_widget)

        self.statusBar()

        self._viewer_controller = ViewerController()

        self._message_box = MessageBox(self)
        self._path_navigator = PathNavigator(self)
        self._file_name_label = QtWidgets.QLabel()
        self._file_counter_label = QtWidgets.QLabel()
        self._directory_toc = DirectoryTocWidget()
        image_widget = self._viewer_controller.image_widget

        # Fixme: add funcs ?
        self._document_widgets = (
            self._file_name_label,
            self._file_counter_label,
            image_widget,
        )

        self._vertical_layout = QtWidgets.QVBoxLayout(self._central_widget)
        self._vertical_layout.addWidget(self._message_box)
        self._vertical_layout.addWidget(self._path_navigator)
        horizontal_layout = QtWidgets.QHBoxLayout()
        # Fixme: layout
        horizontal_layout.addWidget(self._file_name_label)
        horizontal_layout.addWidget(self._file_counter_label)
        self._vertical_layout.addLayout(horizontal_layout)
        self._vertical_layout.addWidget(self._directory_toc)
        self._vertical_layout.addWidget(image_widget)

        self._directory_list = DirectoryListWidget(self)
        self._directory_list_dock_widget = self._create_dock(
            'Move Document',
            self._directory_list,
            self.HORIZONTAL_DOCK_AREA,
            Qt.LeftDockWidgetArea,
        )

        search_panel_widget = self._create_qml_view('SearchPanel.qml', minimum_size=(500, 300))
        search_panel = search_panel_widget.rootObject()
        self._search_dock = self._create_dock(
            'Search Document',
            search_panel_widget,
            self.HORIZONTAL_DOCK_AREA,
            Qt.RightDockWidgetArea,
        )

        document_metadata_widget = self._create_qml_view('DocumentMetadataPanel.qml', minimum_size=(500, 300))
        document_metadata_panel = document_metadata_widget.rootObject()
        search_panel.document_clicked.connect(document_metadata_panel.set_document)
        search_panel.document_clicked.connect(self._show_document)
        self._document_metadata_dock = self._create_dock(
            'Document Metadata',
            document_metadata_widget,
            self.HORIZONTAL_DOCK_AREA,
            Qt.RightDockWidgetArea,
        )

        self._path_navigator.path_changed.connect(self.open_directory)
        self._directory_toc.path_changed.connect(self.open_directory)
        self._directory_list.move_file.connect(self.move_file)
        self._directory_list.move_current_file.connect(self.move_current_file)

        self._create_actions()
        self._create_toolbar()

        self._directory_toc_mode()

    ##############################################

    def _create_dock(self, title, widget, allowed_area, area):

        dock_widget = QtWidgets.QDockWidget(title, self)
        dock_widget.setAllowedAreas(allowed_area)
        dock_widget.setWidget(widget)
        self.addDockWidget(area, dock_widget)

        return dock_widget

    ##############################################

    def _create_qml_view(self, qml_file, minimum_size=(0,0)):

        path = str(ConfigInstall.Path.join_qml_path(qml_file))

        widget = QQuickWidget(self.qml_engine, self)
        # The view will automatically resize the root item to the size of the view.
        widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        # The view resizes with the root item in the QML.
        # widget.setResizeMode(QQuickWidget.SizeViewToRootObject)
        widget.setSource(QUrl(path))
        widget.resize(*minimum_size)

        return widget

    ##############################################

    def _create_actions(self):

        icon_loader = IconLoader()

        self._directory_toc_mode_action = QtWidgets.QAction(
            icon_loader['folder-open-black@36'],
            'Directory toc mode',
            self,
            toolTip=self._tr('Directory toc mode'),
            triggered=self._directory_toc_mode,
            shortcut='Ctrl+D',
            shortcutContext=Qt.ApplicationShortcut,
        )

        self._pdf_browser_mode_action = QtWidgets.QAction(
            icon_loader['book-black@36'], # application-pdf
            'PDF browser mode',
            self,
            toolTip=self._tr('PDF browser mode'),
            triggered=self._pdf_browser_mode,
            shortcut='Ctrl+P',
            shortcutContext=Qt.ApplicationShortcut,
        )

        self._search_dock_action = self._search_dock.toggleViewAction()
        self._search_dock_action.setIcon(icon_loader['search-black@36'])
        self._search_dock_action.setToolTip(self._tr('Toggle Search Panel'))

        self._document_metadata_dock_action = self._document_metadata_dock.toggleViewAction()
        self._document_metadata_dock_action.setIcon(icon_loader['description-black@36'])
        self._document_metadata_dock_action.setToolTip(self._tr('Toggle Metadata Panel'))

        self._previous_document_action = QtWidgets.QAction(
            icon_loader['chevron-left-black@36'],
            'Previous document',
            self,
            toolTip=self._tr('Previous Document'),
            triggered=self.previous_document,
            shortcut='Backspace',
            shortcutContext=Qt.ApplicationShortcut,
        )

        self._next_document_action = QtWidgets.QAction(
            icon_loader['chevron-right-black@36'],
            'Next document',
            self,
            toolTip=self._tr('Next Document'),
            triggered=self.next_document,
            shortcut='Space',
            shortcutContext=Qt.ApplicationShortcut,
        )

        self._select_action = QtWidgets.QAction(
            icon_loader['star-black@36'],
            'Select document',
            self,
            toolTip=self._tr('Select Document'),
            triggered=self.select_document,
            shortcut='Ctrl+S',
            shortcutContext=Qt.ApplicationShortcut,
        )

        self._open_pdf_action = QtWidgets.QAction(
            icon_loader['open-in-new-black@36'],
            'Open PDF',
            self,
            toolTip=self._tr('Open PDF'),
            triggered=lambda x: self.open_current_document(extern=True),
            shortcut='Ctrl+O',
            shortcutContext=Qt.ApplicationShortcut,
        )

        self._open_pdf_viewer_action = QtWidgets.QAction(
            icon_loader['description-black@36'],
            'Open PDF Viewer',
            self,
            toolTip=self._tr('Open PDF Viewer'),
            triggered=lambda x: self.open_current_document(extern=False),
            shortcut='Ctrl+V',
            shortcutContext=Qt.ApplicationShortcut,
        )

    ##############################################

    def _create_toolbar(self):

        self._main_tool_bar = self.addToolBar('Main')
        for item in (
                self._search_dock_action,
                self._document_metadata_dock_action,
                self._directory_toc_mode_action,
                self._pdf_browser_mode_action,
        ):
            self._main_tool_bar.addAction(item)

        self._document_tool_bar = self.addToolBar('Document')
        for item in (
                self._previous_document_action,
                self._next_document_action,
                self._select_action,
                self._open_pdf_action,
                self._open_pdf_viewer_action,
        ):
            self._document_tool_bar.addAction(item)

        self.addToolBar(self._viewer_controller.tool_bar)
        self.addToolBar(self._viewer_controller.page_controller.tool_bar)

    ##############################################

    def init_menu(self):

        super(PdfBrowserMainWindow, self).init_menu()

    ##############################################

    def show_message(self, message=None, timeout=0, warn=False):

        """Hides the normal status indications and displays the given message for the specified number of
        milli-seconds (timeout). If timeout is 0 (default), the message remains displayed until the
        clearMessage() slot is called or until the showMessage() slot is called again to change the
        message.

        Note that showMessage() is called to show temporary explanations of tool tip texts, so
        passing a timeout of 0 is not sufficient to display a permanent message.

        """

        if warn:
            self._message_box.push_message(message)
        else:
            status_bar = self.statusBar()
            if message is None:
                status_bar.clearMessage()
            else:
                status_bar.showMessage(message, timeout)

    ##############################################

    def _directory_toc_mode(self):

        self._directory_toc.show()
        for widget in self._document_widgets:
            widget.hide()

    ##############################################

    def _pdf_browser_mode(self):

        self._directory_toc.hide()
        for widget in self._document_widgets:
            widget.show()

    ##############################################

    def open_directory(self, path):

        self._logger.info("open directory {}".format(str(path)))
        # Fixme: move to application?
        self._current_path = path
        self._directory_toc.update(DirectoryToc(path))
        self._path_navigator.set_path(path) # Fixme: path_navigator -> open_directory -> path_navigator
        self._document_directory = DocumentDirectory(path)
        if bool(self._document_directory):
            self._show_document()
        else:
            for widget in self._document_widgets:
                widget.clear()

    ##############################################

    @property
    def current_path(self):

        return self._current_path

    ##############################################

    @property
    def current_document(self):

        return self._document_directory.current_item

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
            # Fixme: document_directory -~-> document changed
            next(self._document_directory)
            self._show_document()
        except StopIteration:
            pass

    ##############################################

    def _show_document(self, document=None):

        if document is not None:
            row = document.row
            document_root_path = Directory(self.application.config.Path.DOCUMENT_ROOT_PATH)
            absolut_path = document_root_path.join_filename(row.path)
            parent_path = absolut_path.directory
            self.open_directory(parent_path)
            _ = self._document_directory.rotate_to_path(absolut_path)
            self._logger.info('show document\n{}\n{}'.format(absolut_path, _))
            self._pdf_browser_mode()

        try:
            document = self.current_document
            self._logger.info('current_document {}'.format(document.path))
            self._file_name_label.setText(str(document.path.filename_part()))
            self._file_counter_label.setText('{} / {}'.format(
                self._document_directory.current_index +1,
                len(self._document_directory)),
            )
            self._viewer_controller.document = document.document # Fixme:
        except EmptyRingError:
            # self._logger.info('EmptyRingError')
            # Fixme: cf. open_directory
            for widget in self._document_widgets:
                widget.clear()

    ##############################################

    def select_document(self):

        pass
        # try:
        #     document = self.current_document
        #     document.selected = not document.selected
        #     self._viewer_controller.update_style()
        # except EmptyRingError:
        #     pass

    ##############################################

    def open_current_document(self, extern=True):

        try:
            document = self.current_document
            document_path = str(document.path)
            if extern:
                subprocess.call(('xdg-open', document_path))
            else:
                from Babel.GUI.PdfViewer.PdfViewerMainWindow import PdfViewerMainWindow
                pdf_viewer_window = PdfViewerMainWindow(document_path, parent=self)
                pdf_viewer_window.showMaximized()
        except EmptyRingError:
            pass

    ##############################################

    def _delete_file_from_browser(self, file_path):

        current_document = self.current_document # should not raise EmptyRingError
        if current_document.path != file_path:
            self._document_directory.delete(current_document)
        else:
            if not self._document_directory.delete_path(file_path):
                raise NameError("File {} not in the current directory".format(file_path))
        self._show_document()

    ##############################################

    def move_current_file(self, dst_path):

        self.move_file(self.current_document.path, dst_path)

    ##############################################

    def move_file(self, file_path, dst_path):

        # Fixme: here ?

        to_file_path = dst_path.join_filename(file_path.filename_part())

        # Test if the destination directory has already a file with the same name
        overwrite = False
        if bool(to_file_path):
            if file_path.shasum == to_file_path.shasum:
                # self.show_message("Destination has a duplicate of this file", warn=True)
                rc = QtWidgets.QMessageBox.question(
                    self,
                    "",
                    "Destination has a duplicate of this file.\n"
                    "Remove this file instead?"
                )
                if rc == QtWidgets.QMessageBox.Yes:
                    self._logger.info("Delete {}".format(str(file_path)))
                    file_path.delete()
                    self._delete_file_from_browser(file_path)
                return # delete or do nothing
            else:
                # self.show_message("Destination has a file with the same name", warn=True)
                to_file_path2 = AutomaticFileRename(to_file_path).generate()
                filename, ok = QtWidgets.QInputDialog.getText(
                    self,
                    "Destination has a file with the same name",
                    "Rename to:",
                    text=to_file_path2.filename
                )
                # Fixme: implement overwrite
                if ok:
                     to_file_path = dst_path.join_filename(filename)
                else:
                    return # do nothing

        if file_path == to_file_path:
            self.show_message("Tried to move file {} to same place".format(str(file_path)), warn=True)
        else:
            # Last check
            if bool(to_file_path) and not overwrite:
                self.show_message("Tried to overwrite file {}".format(str(file_path)), warn=True)

            self._logger.info("Move {} to {}".format(str(file_path), str(to_file_path)))
            os.rename(str(file_path), str(to_file_path))
            self._delete_file_from_browser(file_path)
