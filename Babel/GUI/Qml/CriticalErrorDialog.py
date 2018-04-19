####################################################################################################
#
# Babel - An Electronic Document Management System
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

import sys
import traceback

from PyQt5 import QtWidgets, QtCore

####################################################################################################

from Babel.Logging.ExceptionHook import format_exception
import Babel.Tools.BackTrace as BackTrace
from .QmlDialog import QmlDialog

####################################################################################################

class CriticalErrorDialog(QmlDialog):

    ###############################################

    def __init__(self, exception_type, exception_value, exception_backtrace, qml_engine=None):

        super().__init__('CriticalErrorDialog', qml_engine)

        # self._backtrace = format_exception(
        #     self._exception_type,
        #     self._exception_value,
        #     self._exception_backtrace,
        # )

        backtrace_text = ''.join(traceback.format_exception(
            exception_type,
            exception_value,
            exception_backtrace,
        ))
        backtrace_html = BackTrace.html_highlight_backtrace(backtrace_text)

        self.root_object.setProperty('backtrace', backtrace_html)

        # Fixme: call critical exit
        self.root_object.exit_application.connect(self._exit_application)

        # title = str(exception_value)
        # error_message_label.setText(title[:50])

    ##############################################

    def _exit_application(self):
        self.done(-1)
