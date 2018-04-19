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

import logging

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtWidgets import QDialog

from Babel.Config import ConfigInstall

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class QmlDialog(QDialog):

    ###############################################

    def __init__(self, qml_file, qml_engine=None):

        super().__init__()

        path = str(ConfigInstall.Path.join_qml_path(qml_file + '.qml'))

        if qml_engine is not None:
            widget = QQuickWidget(qml_engine, self)
        else:
            widget = QQuickWidget(self)
        # The view will automatically resize the root item to the size of the view.
        widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        # The view resizes with the root item in the QML.
        # widget.setResizeMode(QQuickWidget.SizeViewToRootObject)
        widget.setSource(QUrl(path))
        # widget.resize(*minimum_size)

        root_object = widget.rootObject()
        root_object.accepted.connect(self.accept)
        root_object.rejected.connect(self.reject)

        self._widget = widget
        self._root_object = root_object

    ##############################################

    @property
    def root_object(self):
        return self._root_object
