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
from PyQt5.QtWidgets import (
    QAction, QApplication, QMessageBox, QSplashScreen,
)

####################################################################################################

from Babel.Application.ApplicationBase import ApplicationBase
import Babel.Config.Config as Config
import Babel.Config.ConfigInstall as ConfigInstall
import Babel.Config.Messages as Messages
import Babel.Version as Version
from ..Forms.CriticalErrorForm import CriticalErrorForm
from .ApplicationStyle import ApplicationStyle

# Load RC
#import Babel.gui.ui.babel_rc

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
        if not QResource.registerResource(rcc_path):
            self._logger.debug('Failed to load ressource {}'.format(rcc_path))

        self._application_style = ApplicationStyle()

        self._display_splash_screen()

        self._main_window = None
        self._init_actions()

    ##############################################

    @property
    def main_window(self):
        return self._main_window

    @property
    def application_style(self):
        return self._application_style

    ##############################################

    def _exception_hook(self, exception_type, exception_value, exception_traceback):

        traceback.print_exception(exception_type, exception_value, exception_traceback)
        dialog = CriticalErrorForm(exception_type, exception_value, exception_traceback)
        dialog.exec_()

        # return sys.__excepthook__(exception_type, exception_value, exception_traceback)

    ##############################################

    def _display_splash_screen(self):

        pixmap = QPixmap(':/splash screen/images/splash_screen.png')
        self._splash = QSplashScreen(pixmap)
        self._splash.show()
        self._splash.showMessage('<h2>Babel %(version)s</h2>' % {'version':str(Version.babel)})
        self.processEvents()

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

        self._splash.finish(self._main_window)
        self.processEvents()
        del self._splash

        QTimer.singleShot(0, self.execute_given_user_script)

        self.show_message('Welcome to Babel')

        # return to main and then enter to event loop

    ##############################################

    def show_message(self, message=None, echo=False, timeout=0):

        # Fixme: cf. PdfBrowserApplication
        if self._main_window is not None:
            self._main_window.show_message(message, echo, timeout)

    ##############################################

    # Fixme: CriticalErrorForm vs critical_error

    def critical_error(self, title='Babel Critical Error', message=''):

        QMessageBox.critical(None, title, message)

        # Fixme: qt close?
        sys.exit(1)

    ##############################################

    def open_help(self):

        url = QUrl()
        url.setScheme(Config.Help.url_scheme)
        url.setHost(Config.Help.host)
        url.setPath(Config.Help.url_path_pattern) # % str(Version.babel))
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

    ###############################################

    def send_email(self):

        dialog = EmailBugForm()
        dialog.exec_()
