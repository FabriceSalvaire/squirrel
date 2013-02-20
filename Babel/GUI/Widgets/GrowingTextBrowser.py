####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

from PyQt4 import QtCore, QtGui

####################################################################################################

class GrowingTextBrowser(QtGui.QTextBrowser):

    _id = 0

    ##############################################

    def __init__(self, *args, **kwargs):

        GrowingTextBrowser._id += 1
        self._id = GrowingTextBrowser._id

        super(GrowingTextBrowser, self).__init__(*args, **kwargs)  
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
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
        print "Document width", document_size.width(), 'height', document_size.height()

    ##############################################

    def sizePolicy(self):

        size_policy = super(GrowingTextBrowser, self).sizePolicy()
        print 'GrowingTextBrowser.sizePolicy', self._id, \
            size_policy.horizontalPolicy(), size_policy.verticalPolicy()
        return size_policy

    ##############################################

    def sizeHint(self):

        size = super(GrowingTextBrowser, self).sizeHint()
        print 'GrowingTextBrowser.sizeHint', self._id, size.width(), size.height()
        return QtCore.QSize(0, 0)

    ##############################################

    def minimumSizeHint(self):

        size = super(GrowingTextBrowser, self).minimumSizeHint()
        print 'GrowingTextBrowser.minimumSizeHint', self._id, size.width(), size.height()
        return QtCore.QSize(0, 0)

    ##############################################

    def heightForWidth(self, width):

        print 'GrowingTextBrowser.heightForWidth', self._id, width
        document = QtGui.QTextDocument(self._text)
        document.setPageSize(QtCore.QSizeF(width, -1))
        height = document.documentLayout().documentSize().toSize().height()
        self.print_document_size(document)
        return height + self.font().pointSize()

    ##############################################

    def resizeEvent(self, event):

        print 'GrowingTextBrowser.resizeEvent', self._id, \
            'old', event.oldSize().width(), event.oldSize().height(), \
            'new', event.size().width(), event.size().height()
        self.print_document_size()
        return super(GrowingTextBrowser, self).resizeEvent(event)

####################################################################################################
# 
# End
# 
####################################################################################################
