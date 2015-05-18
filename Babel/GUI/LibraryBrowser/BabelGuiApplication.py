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

import logging

from PyQt5 import QtCore, QtWidgets

####################################################################################################

from Babel.GUI.Base.GuiApplicationBase import GuiApplicationBase
from Babel.Application.BabelApplication import BabelApplication

####################################################################################################

class BabelGuiApplication(GuiApplicationBase, BabelApplication):

    _logger = logging.getLogger(__name__)
    
    ###############################################
    
    def __init__(self, args):

        #
        # <class 'Babel.GUI.BabelGuiApplication.BabelGuiApplication'>
        # <class 'Babel.GUI.GuiApplicationBase.GuiApplicationBase'>
        # <class 'Babel.Application.BabelApplication.BabelApplication'>
        # <class 'Babel.Application.ApplicationBase.ApplicationBase'>
        # <class 'PyQt5.QtWidgets.QApplication'>
        # <class 'PyQt5.QtCore.QCoreApplication'>
        # <class 'PyQt5.QtCore.QObject'>
        # <type 'sip.wrapper'>
        # <type 'sip.simplewrapper'>
        # <type 'object'>
        # 
        # ApplicationBase.__init__
        # BabelApplication.__init__
        # QtWidgets.QApplication
        # GuiApplicationBase.__init__
        # BabelGuiApplication.__init__
        #

        super(BabelGuiApplication, self).__init__(args=args)
        self._logger.debug(str(args))
        
        from .BabelMainWindow import MainWindow
        self._main_window = MainWindow()
        self._main_window.showMaximized()
        
        self.post_init()

    ##############################################

    def _init_actions(self):

        super(BabelGuiApplication, self)._init_actions()

        self.open_files_action = \
            QtWidgets.QAction('Open Files',
                          self,
                          triggered=self.open_files)

    ##############################################
 
    def open_files(self):
 
        dialog = QtWidgets.QFileDialog.getOpenFileName
        files = dialog(self.main_window, 'Open Files')

    ##############################################

    def open_pdf(self, path):
       
        path = path.absolut()
        self._logger.info("Open PDF %s" % (str(path)))

        from Babel.GUI.PdfViewer.PdfViewerMainWindow import PdfViewerMainWindow
        pdf_viewer_main_window = PdfViewerMainWindow(path, parent=self._main_window)
        pdf_viewer_main_window.showMaximized()

####################################################################################################
#
# End
#
####################################################################################################
