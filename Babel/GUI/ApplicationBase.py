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

from Babel.Tools.PathTools import to_absolute_path
from Babel.Tools.Platform import Platform
from Babel.GUI.CriticalErrorForm import CriticalErrorForm
from Babel.GUI.EmailBugForm import EmailBugForm
#import Config
import Babel.Version as Version
#import BabelMessages

# Load RC
#import Babel.gui.ui.babel_rc

####################################################################################################

system_information_message_pattern = """
<h2>Babel %(babel_version)s</h2>
<h2>Host %(node)s</h2>
<h3>Hardware</h3>
<ul>
<li>Machine: %(machine)s</li>
<li>Architecture: %(architecture)s</li>
<li>CPU: %(cpu)s</li>
<li>Number of cores: %(number_of_cores)u</li>
<li>Memory Size: %(memory_size)u MB</li>
</ul>
<h3>OpenGL</h3>
<ul>
<li>Render: %(gl_renderer)s</li>
<li>Version: %(gl_version)s</li>
<li>Vendor: %(gl_vendor)s</li>
</ul>
<h3>Software Versions</h3>
<ul>
<li>OS: %(os)s %(distribution)s</li>
<li>Python %(python_version)s</li>
<li>Qt %(qt_version)s</li>
<li>PyQt %(pyqt_version)s</li>
</ul>
"""

####################################################################################################

class ApplicationBase(QtGui.QApplication):
    
    ##############################################
    
    def __init__(self, args):

        super(ApplicationBase, self).__init__(sys.argv)

        sys.excepthook = self._exception_hook

        self.args = args

        self._display_splash_screen()

        self.main_window = None
        self.platform = Platform(self)
        
        self._init_actions()

    ##############################################

    def _exception_hook(self, exception_type, exception_value, exception_traceback):

        # print 'ApplicationBase._exception_hook'

        print traceback.print_exception(exception_type, exception_value, exception_traceback)
        dialog = CriticalErrorForm(exception_type, exception_value, exception_traceback)
        dialog.exec_()

        # return sys.__excepthook__(exception_type, exception_value, exception_traceback)

    ##############################################

    def _display_splash_screen(self):

        print 'Babel start ...'
        pixmap = QtGui.QPixmap(':/splash screen/images/splash_screen.png')
        self.splash = QtGui.QSplashScreen(pixmap)
        self.splash.show()
        # self.splash.showMessage('<h2>Babel %(version)s</h2>' % {'version':str(Version.babel)})
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
         
        self.splash.finish(self.main_window)
        self.processEvents()
        del self.splash

        QtCore.QTimer.singleShot(0, self._execute_user_script_slot)

        # return to main and then enter to event loop

    ##############################################
    
    def _execute_user_script_slot(self):

        if self.args.user_script is not None:
            self.execute_user_script(self.args.user_script)
        
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

        if self.main_window is not None:
            self.main_window.show_message(message, echo, timeout)

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
        url.setPath(Config.Help.url_path_pattern % str(Version.babel))
        QtGui.QDesktopServices.openUrl(url)

    ##############################################

    def about(self):
        
        message = BabelMessages.about_babel % {'version':str(Version.babel)}
        QtGui.QMessageBox.about(self.main_window, 'About Babel', message)

    ##############################################

    def show_system_information(self):

        # Fixme: add getattr method to Platform
        platform = self.platform
        fields = {'node': platform.node,
                  'os': platform.os,
                  'distribution': platform.distribution,
                  'cpu': platform.cpu,
                  'machine': platform.machine,
                  'architecture': platform.architecture,
                   'number_of_cores': 0, # Fixme: platform.number_of_cores,
                  'memory_size': platform.memory_size_kb/1024,
                  'gl_renderer': platform.gl_renderer,
                  'gl_version': platform.gl_version,
                  'gl_vendor': platform.gl_vendor,
                  'gl_extensions': platform.gl_extensions,
                  'python_version': platform.python_version,
                  'qt_version': platform.qt_version,
                  'pyqt_version': platform.pyqt_version,
                  'babel_version': str(Version.babel),
                  }

        message = system_information_message_pattern % fields
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
