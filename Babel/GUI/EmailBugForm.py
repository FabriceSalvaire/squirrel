# -*- coding: utf-8 -*-

####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

from PyQt4 import QtGui

####################################################################################################

from Babel.Logging.Email import Email
from Babel.Tools.Platform import Platform
#import Config
import Babel.Version as Version

####################################################################################################

from Babel.GUI.ui.email_bug_form_ui import Ui_email_bug_form

####################################################################################################

class EmailBugForm(QtGui.QDialog):

    ###############################################

    def __init__(self, traceback=''):

        super(EmailBugForm, self).__init__()

        self._traceback = traceback

        form = self.form = Ui_email_bug_form()
        form.setupUi(self)

        form.send_email_button.clicked.connect(self.send_email)

    ##############################################

    def send_email(self):

        form = self.form

        from_address = str(form.from_line_edit.text())
        if not from_address:
            from_address = Config.Email.from_address
        
        # Fixme: test field ?
        # QtGui.QMessageBox.critical(None, title, message)

        template_message = '''
Bug description:
%(description)s

---------------------------------------------------------------------------------
Babel Version:
  %(babel_version)s

---------------------------------------------------------------------------------
Slide Information:

  Slide:       %(slide_file_name)s
  SQlite File: %(sqlite_file_name)s

---------------------------------------------------------------------------------
%(traceback)s

---------------------------------------------------------------------------------
%(platform)s

---------------------------------------------------------------------------------
'''   

        application = QtGui.QApplication.instance()

        # Fixme: singleton ?
        platform = Platform(application)
        platform.query_opengl()

        if hasattr(application, 'slide') and application.slide is not None:
            slide_file_name = application.slide.slide_path.slide_file_name()
        else:
            slide_file_name = str(None)

        if hasattr(application, 'sqlitedb') and  application.sqlitedb is not None:
            sqlite_file_name = application.sqlitedb.filename
        else:
            sqlite_file_name = str(None)
        
        message = template_message % {'description': str(form.description_plain_text_edit.toPlainText()),
                                      'slide_file_name': slide_file_name,
                                      'sqlite_file_name': sqlite_file_name,
                                      'babel_version': str(Version.babel),
                                      'platform': str(platform),
                                      'traceback': self._traceback,
                                      }

        email = Email(from_address=from_address,
                      subject='Babel Bug: ' + str(form.subject_line_edit.text()),
                      recipients=Config.Email.to_address,
                      message=message,
                      )
        recipients = str(form.recipients_line_edit.text())
        if recipients:
            email.add_recipients_from_string(recipients)
        email.send()

        self.accept()

####################################################################################################
#
# End
#
####################################################################################################
