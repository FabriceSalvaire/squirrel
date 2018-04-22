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
#
# If an exception is raise before application.exec then application exit.
#
####################################################################################################

####################################################################################################

import logging
import sys
import traceback

from PyQt5.QtCore import Qt, QResource, QTimer, QUrl
from PyQt5.QtGui import QDesktopServices, QPixmap
from PyQt5.QtQml import QQmlEngine
from PyQt5.QtWidgets import (
    QAction, QApplication, QMessageBox, QSplashScreen,
)

####################################################################################################

from ..Qml.ApplicationStyle import ApplicationStyle
from ..Qml.CriticalErrorDialog import CriticalErrorDialog
from ..Widgets.IconLoader import IconProvider
from Babel.Application.ApplicationBase import ApplicationBase
import Babel.Config.ConfigInstall as ConfigInstall
import Babel.Config.DefaultConfig as DefaultConfig # Fixme: for Help
import Babel.Config.Messages as Messages
import Babel.Version as Version

####################################################################################################

class GuiApplicationBase(ApplicationBase, QApplication):

    _logger = logging.getLogger(__name__)

    has_gui = True

    ##############################################

    def __init__(self, args, **kwargs):

        super(GuiApplicationBase, self).__init__(args=args, **kwargs)
        # Fixme: Why ?
        self._logger.debug("QApplication " + str(sys.argv))
        QApplication.__init__(self, sys.argv)
        self._logger.debug('GuiApplicationBase ' + str(args) + ' ' + str(kwargs))

        self.setAttribute(Qt.AA_EnableHighDpiScaling)

        # from . import BabelRessource
        rcc_path = ConfigInstall.Path.join_share_directory('babel.rcc')
        self._logger.debug('Load ressource {}'.format(rcc_path))
        if not QResource.registerResource(str(rcc_path)):
            self._logger.debug('Failed to load ressource {}'.format(rcc_path))

        # self._display_splash_screen()

        self._main_window = None
        self._initialise_qml_engine()
        self._init_actions()

    ##############################################

    @property
    def main_window(self):
        return self._main_window

    @property
    def qml_engine(self):
        return self._qml_engine

    @property
    def qml_context(self):
        return self._qml_engine.rootContext()

    ##############################################

    def _exception_hook(self, exception_type, exception_value, exception_traceback):

        traceback.print_exception(exception_type, exception_value, exception_traceback)
        dialog = CriticalErrorDialog(
            exception_type, exception_value, exception_traceback,
            qml_engine=self._qml_engine
        )
        rc = dialog.exec_()
        if rc == -1:
            self.exit()

        # return sys.__excepthook__(exception_type, exception_value, exception_traceback)

    ##############################################

    def _display_splash_screen(self):

        pixmap = QPixmap(':/splash screen/images/splash_screen.png')
        self._splash = QSplashScreen(pixmap)
        self._splash.show()
        self._splash.showMessage('<h2>Babel %(version)s</h2>' % {'version':str(Version.babel)})
        self.processEvents()

    ##############################################

    def _initialise_qml_engine(self):

        self._qml_engine = QQmlEngine(self)

        qml_path = str(ConfigInstall.Path.qml_path)
        self._qml_engine.addImportPath(qml_path)

        context = self.qml_context
        self._application_style = ApplicationStyle()
        context.setContextProperty('application_style', self._application_style)

        self._icon_provider = IconProvider()
        self._qml_engine.addImageProvider('icon_provider', self._icon_provider)

    ##############################################

    def _init_actions(self):

        self.about_action = QAction(
            'About Babel',
            self,
            triggered=self.about,
        )

        self.exit_action = QAction(
            'Exit',
            self,
            triggered=self.exit,
        )

        self.help_action = QAction(
            'Help',
            self,
            triggered=self.open_help,
        )

        self.show_system_information_action = QAction(
            'System Information',
            self,
            triggered=self.show_system_information,
        )

    ##############################################

    def post_init(self):

        # self._splash.finish(self._main_window)
        # self.processEvents()
        # del self._splash

        QTimer.singleShot(0, self.execute_given_user_script)

        self.show_message('Welcome to Babel')

        # return to main and then enter to event loop

    ##############################################

    def show_message(self, message=None, echo=False, timeout=0):

        # Fixme: cf. PdfBrowserApplication
        if self._main_window is not None:
            self._main_window.show_message(message, echo, timeout)

    ##############################################

#    def critical_error(self, title='Babel Critical Error', message=''):
#
#        # Fixme: CriticalErrorForm vs critical_error
#
#        QMessageBox.critical(None, title, message)
#
#        # Fixme: qt close?
#        sys.exit(1)

    ##############################################

    def open_help(self):

        url = QUrl()
        url.setScheme(DefaultConfig.Help.url_scheme)
        url.setHost(DefaultConfig.Help.host)
        url.setPath(DefaultConfig.Help.url_path_pattern) # % str(Version.babel))
        QDesktopServices.openUrl(url)

    ##############################################

    def about(self):

        message = Messages.about_babel % {'version':str(Version.babel)}
        QMessageBox.about(self.main_window, 'About Babel', message)

    ##############################################

    def show_system_information(self):

        fields = dict(self._platform.__dict__)
        fields.update({
                'babel_version': str(Version.babel),
                })
        message = Messages.system_information_message_pattern % fields
        QMessageBox.about(self.main_window, 'System Information', message)
