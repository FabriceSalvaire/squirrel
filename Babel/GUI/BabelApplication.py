####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

###################################################################################################

from PyQt4 import QtCore

####################################################################################################

from Babel.GUI.ApplicationBase import ApplicationBase

####################################################################################################

class BabelApplication(ApplicationBase):
    
    ###############################################
    
    def __init__(self, args):
         
         super(BabelApplication, self).__init__(args)

         from Babel.GUI.BabelMainWindow import MainWindow
         self.main_window = MainWindow()
         self.main_window.showMaximized()
       
         self.post_init()

    ##############################################

    def show_message(self, message=None, echo=False, timeout=0):

        self.main_window.show_message(message, echo)
         
####################################################################################################
#
# End
#
####################################################################################################
