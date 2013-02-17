# -*- coding: utf-8 -*-

####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################
#
#                                              Audit
#
# - 13/02/2013 Fabrice
#   - check close
#
####################################################################################################

####################################################################################################

from PyQt4 import QtGui, QtCore

####################################################################################################

class MainWindowBase(QtGui.QMainWindow):
    
    ##############################################
    
    def __init__(self, title=''):

        super(MainWindowBase, self).__init__()

        self.setWindowTitle(title)

        self._application = QtGui.QApplication.instance()
        self.init_menu()

    ##############################################

    @property
    def application(self):
        return self._application

    @property
    def menu_bar(self):
        return self.menuBar()

    @property
    def file_menu(self):
        return self._file_menu

    @property
    def help_menu(self):
        return self._help_menu

    ##############################################

    def init_menu(self):

        application = self._application

        self._file_menu = file_menu = self.menu_bar.addMenu('File')
        file_menu.addAction(application.exit_action) # Fixme: At the end
        
        self._help_menu = help_menu = self.menu_bar.addMenu('Help')
        help_menu.addAction(application.help_action)
        help_menu.addSeparator()
        help_menu.addAction(application.about_action)
        help_menu.addAction(application.show_system_information_action)
        help_menu.addAction(application.send_email_action)

    ##############################################

    def closeEvent(self, event=None):

        self._application.exit()

    ##############################################

    def show_message(self, message=None, echo=False, timeout=0):

        status_bar = self.statusBar()
        if message is None:
            status_bar.clearMessage()
        else:
            status_bar.showMessage(message, timeout)

        # self.application.processEvents()

####################################################################################################
#
# End
#
####################################################################################################
