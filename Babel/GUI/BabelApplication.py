####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

###################################################################################################

from PyQt4 import QtCore, QtGui

####################################################################################################

from Babel.GUI.ApplicationBase import ApplicationBase

####################################################################################################

class BabelApplication(ApplicationBase):
    
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

####################################################################################################
#
# End
#
####################################################################################################
