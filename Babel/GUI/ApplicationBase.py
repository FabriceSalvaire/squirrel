# -*- coding: utf-8 -*-

####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

###################################################################################################
#
# If an exception is raise before application.exec then application exit.
#
####################################################################################################

####################################################################################################

import sys
import traceback

from PyQt4 import QtGui, QtCore

####################################################################################################

from Babel.GUI.CriticalErrorForm import CriticalErrorForm
from Babel.GUI.EmailBugForm import EmailBugForm
from Babel.Tools.Path import to_absolute_path
from Babel.Tools.Platform import Platform
import Babel.Config.Config as Config
import Babel.Config.Messages as Messages
import Babel.Version as Version

# Load RC
#import Babel.gui.ui.babel_rc

####################################################################################################

####################################################################################################

class ApplicationBase(QtGui.QApplication):
    
    ##############################################
    
    def __init__(self, args):

        super(ApplicationBase, self).__init__(sys.argv)

        sys.excepthook = self._exception_hook
        self._display_splash_screen()

        self._args = args
        self._main_window = None
        self._platform = Platform(self)
        self._init_actions()

    ##############################################

    @property
    def args(self):
        return self._args

    @property
    def main_window(self):
        return self._main_window

    @property
    def platform(self):
        return self._platform

    ##############################################

    def _exception_hook(self, exception_type, exception_value, exception_traceback):

        traceback.print_exception(exception_type, exception_value, exception_traceback)
        dialog = CriticalErrorForm(exception_type, exception_value, exception_traceback)
        dialog.exec_()

        # return sys.__excepthook__(exception_type, exception_value, exception_traceback)

    ##############################################

    def _display_splash_screen(self):

        pixmap = QtGui.QPixmap(':/splash screen/images/splash_screen.png')
        self._splash = QtGui.QSplashScreen(pixmap)
        self._splash.show()
        self._splash.showMessage('<h2>Babel %(version)s</h2>' % {'version':str(Version.babel)})
        self.processEvents()

    ##############################################

    def _init_actions(self):

        self.about_action = \
            QtGui.QAction('About Babel',
                          self,
                          triggered=self.about)

        self.exit_action = \
            QtGui.QAction('Exit',
                          self,
                          triggered=self.exit)

        self.help_action = \
            QtGui.QAction('Help',
                          self,
                          triggered=self.open_help)

        self.show_system_information_action = \
            QtGui.QAction('System Information',
                          self,
                          triggered=self.show_system_information)
        
        self.send_email_action = \
            QtGui.QAction('Send Email',
                          self,
                          triggered=self.send_email)

    ##############################################
    
    def post_init(self):
         
        self._splash.finish(self._main_window)
        self.processEvents()
        del self._splash

        QtCore.QTimer.singleShot(0, self._execute_user_script_slot)

        self.show_message('Welcome to Babel')

        # return to main and then enter to event loop

    ##############################################
    
    def _execute_user_script_slot(self):

        if self._args.user_script is not None:
            self.execute_user_script(self._args.user_script)
        
    ##############################################
    
    def execute_user_script(self, file_name):

        """ Execute an user script provided by file *file_name* in a context where is defined a
        variable *application* that is a reference to the application instance.
        """
        
        file_name = to_absolute_path(file_name)
        self.show_message(message='Execute user script: ' + file_name, echo=True)
        source = open(file_name).read()
        bytecode = compile(source, file_name, 'exec')
        exec bytecode in {'application':self}
        self.show_message(message='User script done', echo=True)
        
    ##############################################
    
    def exit(self):

        # Fixme: right?

        sys.exit(0)

    ##############################################

    def show_message(self, message=None, echo=False, timeout=0):

        if self._main_window is not None:
            self._main_window.show_message(message, echo, timeout)

    ##############################################
    
    # Fixme: CriticalErrorForm vs critical_error

    def critical_error(self, title='Babel Critical Error', message=''):
        
        QtGui.QMessageBox.critical(None, title, message)
        
        # Fixme: qt close?
        sys.exit(1)

    ##############################################

    def open_help(self):

        url = QtCore.QUrl()
        url.setScheme(Config.Help.url_scheme)
        url.setHost(Config.Help.host)
        url.setPath(Config.Help.url_path_pattern) # % str(Version.babel))
        QtGui.QDesktopServices.openUrl(url)

    ##############################################

    def about(self):
        
        message = Messages.about_babel % {'version':str(Version.babel)}
        QtGui.QMessageBox.about(self.main_window, 'About Babel', message)

    ##############################################

    def show_system_information(self):

        fields = dict(self._platform.__dict__)
        fields.update({
                'babel_version': str(Version.babel),
                })  
        message = Messages.system_information_message_pattern % fields
        QtGui.QMessageBox.about(self.main_window, 'System Information', message)

    ###############################################

    def send_email(self):
        
        dialog = EmailBugForm()
        dialog.exec_()
        
####################################################################################################
#
# End
#
####################################################################################################
