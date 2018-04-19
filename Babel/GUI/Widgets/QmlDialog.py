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

####################################################################################################

#class QmlDialog:
#
#    _logger = _module_logger.getChild('QmlDialog')
#
#    # QDialog(QWidget *parent = Q_NULLPTR, Qt::WindowFlags f = Qt::WindowFlags())
#    # ~QDialog()
#    # bool isSizeGripEnabled() const
#    # int  result() const
#    # void setModal(bool modal)
#    # void setResult(int i)
#    # void setSizeGripEnabled(bool)
#    # virtual QSize minimumSizeHint() const override
#    # virtual void  setVisible(bool visible) override
#    # virtual QSize sizeHint() const override
#    # virtual void  accept()
#    # virtual void  done(int r)
#    # virtual int   exec()
#    # virtual void  open()
#    # virtual void  reject()
#    # void accepted()
#    # void finished(int result)
#    # void rejected()
#
#    ##############################################
#
#    def __init__(self, qml_path, qml_engine=None):
#
#        self._view = QQuickView(qml_engine, None)
#
#        self._view.setResizeMode(QQuickView.SizeViewToRootObject)
#
#        path = str(ConfigInstall.Path.join_qml_path(qml_path + '.qml'))
#        self._view.setSource(QUrl.fromLocalFile(path))
#
#        root_object = self._view.rootObject()
#        root_object.accepted.connect(self._on_accepted)
#        root_object.rejected.connect(self._on_rejected)
#
#        self._result = None
#
#    ##############################################
#
#    def _on_accepted(self):
#
#        self._logger.info('Accepted')
#        self._result = True
#        self._view.close()
#
#    ##############################################
#
#    def _on_rejected(self):
#
#        self._logger.info('Rejected')
#        self._result = False
#        self._view.close()
#
#    ##############################################
#
#    def exec_(self):
#        self._view.show()
#
#    ##############################################
#
#    @property
#    def result(self):
#        return self._result
