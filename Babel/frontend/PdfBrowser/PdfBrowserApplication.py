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

###################################################################################################

import logging

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtQml import qmlRegisterType

from Babel.frontend.Base.GuiApplicationBase import GuiApplicationBase
from Babel.frontend.Application.BabelApplication import BabelApplication
from ..Qml.Search import QmlDocument, QmlSearchManager

####################################################################################################

class PdfBrowserApplication(GuiApplicationBase, BabelApplication):

    # Fixme: open sqlite ...

    _logger = logging.getLogger(__name__)

    ###############################################

    def __init__(self, args):
        super(PdfBrowserApplication, self).__init__(args=args)
        self._logger.debug(str(args))
        from .PdfBrowserMainWindow import PdfBrowserMainWindow
        self._main_window = PdfBrowserMainWindow()
        self._main_window.showMaximized()
        self.post_init()

    ##############################################

    def _initialise_qml_engine(self):
        super()._initialise_qml_engine()
        qmlRegisterType(QmlDocument, 'Local', 1, 0, 'Document')
        context = self.qml_context
        self._qml_search_manager = QmlSearchManager(self)
        context.setContextProperty('search_manager', self._qml_search_manager)

    ##############################################

    def _init_actions(self):
        super(PdfBrowserApplication, self)._init_actions()

    ##############################################

    def post_init(self):
        super(PdfBrowserApplication, self).post_init()
        self._main_window.open_directory(self._args.path)

    ##############################################

    def show_message(self, message=None, timeout=0, warn=False):
        """ Hides the normal status indications and displays the given message for the specified
        number of milli-seconds (timeout). If timeout is 0 (default), the message remains displayed
        until the clearMessage() slot is called or until the showMessage() slot is called again to
        change the message.

        Note that showMessage() is called to show temporary explanations of tool tip texts, so
        passing a timeout of 0 is not sufficient to display a permanent message.
        """
        self._main_window.show_message(message, timeout, warn)
