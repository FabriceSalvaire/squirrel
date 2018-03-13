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

from PyQt5 import QtCore, QtGui, QtWidgets

####################################################################################################

class GrowingTextBrowser(QtWidgets.QTextBrowser):

    _id = 0

    ##############################################

    def __init__(self, *args, **kwargs):

        GrowingTextBrowser._id += 1
        self._id = GrowingTextBrowser._id

        super(GrowingTextBrowser, self).__init__(*args, **kwargs)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHeightForWidth(True)
        self.setSizePolicy(size_policy)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    ##############################################

    def setPlainText(self, text):

        super(GrowingTextBrowser, self).setPlainText(text)
        self._text = text

    ##############################################

    def print_document_size(self, document=None):

        if document is None:
            document = self.document()
        document_size = document.size()
        # print "Document width", document_size.width(), 'height', document_size.height()

    ##############################################

    def sizePolicy(self):

        size_policy = super(GrowingTextBrowser, self).sizePolicy()
        # print 'GrowingTextBrowser.sizePolicy', self._id, \
        #     size_policy.horizontalPolicy(), size_policy.verticalPolicy()
        return size_policy

    ##############################################

    def sizeHint(self):

        size = super(GrowingTextBrowser, self).sizeHint()
        # print 'GrowingTextBrowser.sizeHint', self._id, size.width(), size.height()
        return QtCore.QSize(0, 0)

    ##############################################

    def minimumSizeHint(self):

        size = super(GrowingTextBrowser, self).minimumSizeHint()
        # print 'GrowingTextBrowser.minimumSizeHint', self._id, size.width(), size.height()
        return QtCore.QSize(0, 0)

    ##############################################

    def heightForWidth(self, width):

        # print 'GrowingTextBrowser.heightForWidth', self._id, width
        document = QtGui.QTextDocument(self._text)
        document.setPageSize(QtCore.QSizeF(width, -1))
        height = document.documentLayout().documentSize().toSize().height()
        self.print_document_size(document)
        return height + self.font().pointSize()

    ##############################################

    def resizeEvent(self, event):

        # print 'GrowingTextBrowser.resizeEvent', self._id, \
        #     'old', event.oldSize().width(), event.oldSize().height(), \
        #     'new', event.size().width(), event.size().height()
        # self.print_document_size()
        return super(GrowingTextBrowser, self).resizeEvent(event)
