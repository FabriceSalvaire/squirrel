####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

###################################################################################################

import logging

from PyQt4 import QtCore, QtGui

####################################################################################################

from Babel.GUI.ApplicationBase import ApplicationBase

####################################################################################################

class BabelApplication(ApplicationBase):

    _logger = logging.getLogger(__name__)
    
    ###############################################
    
    def __init__(self, args):
         
         super(BabelApplication, self).__init__(args)

         from Babel.GUI.BabelMainWindow import MainWindow
         self._main_window = MainWindow()
         self._main_window.showMaximized()
       
         self.post_init()

    ##############################################

    def _init_actions(self):

        super(BabelApplication, self)._init_actions()

        self.open_files_action = \
            QtGui.QAction('Open Files',
                          self,
                          triggered=self.open_files)

    ##############################################
 
    def open_files(self):
 
        dialog = QtGui.QFileDialog.getOpenFileName
        files = dialog(self.main_window, 'Open Files')

    ##############################################

    def add_files(self):
         
        pass

    ##############################################

    def open_pdf(self, path):
       
        path = path.absolut()
        self._logger.info("Open PDF %s" % (str(path)))

        from Babel.GUI.PdfViewerMainWindow import PdfViewerMainWindow
        pdf_viewer_main_window = PdfViewerMainWindow(path, parent=self._main_window)
        pdf_viewer_main_window.showMaximized()

####################################################################################################
#
# End
#
####################################################################################################
