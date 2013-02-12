# -*- coding: utf-8 -*-

####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

from PyQt4 import QtGui, QtCore

####################################################################################################

from Babel.Tools.Platform import Platform
from Babel.Tools.RedmineRest import RedmineRest

#import Config

####################################################################################################

from Babel.GUI.ui.new_issue_form_ui import Ui_new_issue_form

####################################################################################################

class NewIssueForm(QtGui.QDialog):

    ###############################################

    def __init__(self, traceback=''):

        super(NewIssueForm, self).__init__()

        self._traceback = traceback

        form = self.form = Ui_new_issue_form()
        form.setupUi(self)

        form.ok_button.clicked.connect(self.commit_new_issue)

    ##############################################

    def commit_new_issue(self):

        form = self.form

        subject = str(form.subject_line_edit.text())

        template_description = '''
Bug description:
%(description)s

---------------------------------------------------------------------------------
%(platform)s
---------------------------------------------------------------------------------

%(traceback)s
---------------------------------------------------------------------------------
'''   

        platform = Platform() # Fixme: singleton ?

        description = template_description % {'description': str(form.description_plain_text_edit.toPlainText()),
                                              'platform': str(platform),
                                              'traceback': self._traceback,
                                              }
        
        redmine_rest = RedmineRest(url=Config.RedmineRest.url,
                                   key=Config.RedmineRest.key)

        babel_project = redmine_rest.get_project(Config.RedmineRest.project)

        babel_project.new_issue(subject=subject,
                                description=description,
                                priority_id=None,
                                tracker_id=None,
                                assigned_to_id=None,
                                user_data=None)
        
        self.accept()

####################################################################################################
#
# End
#
####################################################################################################
