# -*- coding: utf-8 -*-

####################################################################################################
# 
# Babel - A Bibliography Manager
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
####################################################################################################

####################################################################################################

from PyQt4 import QtGui, QtCore

####################################################################################################

from Babel.Tools.Platform import Platform
from Babel.Tools.RedmineRest import RedmineRest
import Babel.Config.Config as Config

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
