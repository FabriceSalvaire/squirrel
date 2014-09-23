####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2014
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
        self._logger.debug(str(args))
        
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
