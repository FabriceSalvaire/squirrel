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
# - 11/05/2011 Fabrice
#   - check close
#
####################################################################################################

####################################################################################################

from PyQt4 import QtGui, QtCore

####################################################################################################
#
# Main Window
#

class MainWindowBase(QtGui.QMainWindow):
    
    ##############################################
    
    def __init__(self, title=''):

        super(MainWindowBase, self).__init__()

        self.application = QtGui.QApplication.instance()

        self.setWindowTitle(title)

        self._init_menu()

    ##############################################

    def _init_menu(self):

        application = self.application

        menu_bar = self.menuBar()

        self.file_menu = file_menu = menu_bar.addMenu('File')
        file_menu.addAction(application.exit_action)
        
        self.help_menu = help_menu = menu_bar.addMenu('Help')
        help_menu.addAction(application.help_action)
        help_menu.addSeparator()
        help_menu.addAction(application.about_action)
        help_menu.addAction(application.show_system_information_action)
        help_menu.addAction(application.send_email_action)

    ##############################################

    def init_tabs(self, tab_list):

        self.tab_manager = TabManager(self)
        self.setCentralWidget(self.tab_manager.tab_widget)
        for label, title in tab_list:
            self.tab_manager.add_tab(label, title)

    ##############################################

    def closeEvent(self, event=None):

        # print 'MainWindowBase.closeEvent'

        self.application.exit()

    ##############################################

    def show_message(self, message=None, timeout=0):

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
