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

from PyQt4 import QtCore, QtGui

####################################################################################################

from Babel.GUI.GuiApplicationBase import GuiApplicationBase
from Babel.Application.BabelApplication import BabelApplication

####################################################################################################

class PdfBrowserApplication(GuiApplicationBase, BabelApplication):

    # Fixme: open sqlite ...

    _logger = logging.getLogger(__name__)
    
    ###############################################
    
    def __init__(self, args):


        super(PdfBrowserApplication, self).__init__(args=args)
        self._logger.debug(unicode(args))
        
        from .PdfBrowserMainWindow import PdfBrowserMainWindow
        self._main_window = PdfBrowserMainWindow()
        self._main_window.showMaximized()
        
        self.post_init()

    ##############################################

    def _init_actions(self):

        super(PdfBrowserApplication, self)._init_actions()

    ##############################################

    def post_init(self):

        super(PdfBrowserApplication, self).post_init()
        self._main_window.open_directory(self._args.path)

####################################################################################################
#
# End
#
####################################################################################################
