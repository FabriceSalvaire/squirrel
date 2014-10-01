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

# Notes:
#  DirectoryButton: class, obj, label

####################################################################################################

import logging

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, pyqtSignal

####################################################################################################

from Babel.FileSystem.File import Directory
from Babel.GUI.Widgets.ColumnLayout import ColumnLayout

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class DirectoryButton(QtGui.QPushButton):

    _logger = _module_logger.getChild('DirectoryButton')

    __BULLET_RADIUS__ = 2
    __MARGIN__ = 10
    __LEFT_MARGIN__ = 2 * (__MARGIN__ + __BULLET_RADIUS__)

    clicked = pyqtSignal(Directory)

    ##############################################

    def __init__(self, path, parent=None):

        super(DirectoryButton, self).__init__(parent)

        self.setFocusPolicy(Qt.TabFocus)
        self.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        self.setMinimumHeight(parent.minimumHeight())
        self.setMouseTracking(True)

        self._path = path
        self._label = path.basename()

        self._entered = False

    ##############################################

    @property
    def path(self):
        return self._path

    ##############################################

    def sizeHint(self):

        font = self.font()
        metrics = QtGui.QFontMetrics(font)
        width = metrics.width(self._label) + self.__LEFT_MARGIN__ + self.__MARGIN__
        # height = super(PathNavigatorButton, self).sizeHint().height()
        height = metrics.height()
        # self._logger.info("size hint {} {}".format(width, height))
        return QtCore.QSize(width, height)

    ##############################################

    def enterEvent(self, event):

        super(DirectoryButton, self).enterEvent(event)
        self._entered = True
        self.update()

    ##############################################

    def leaveEvent(self, event):

        super(DirectoryButton, self).leaveEvent(event)
        self._entered = False
        self.update()

    ##############################################

    def mousePressEvent(self, event):

        self.clicked.emit(self._path)
        # super(PathNavigatorButton, self).mousePressEvent(event)

    ##############################################

    def _draw_hover_background(self, painter):

        if self._entered:
            # The QStyleOptionViewItemV4 class is used to describe the parameters necessary for
            # drawing a frame in Qt 4.4 or above.
            option = QtGui.QStyleOptionViewItemV4()
            option.initFrom(self)
            option.state = QtGui.QStyle.State_Enabled | QtGui.QStyle.State_MouseOver
            option.viewItemPosition = QtGui.QStyleOptionViewItemV4.OnlyOne
            self.style().drawPrimitive(QtGui.QStyle.PE_PanelItemViewItem, option, painter, self)

    ##############################################

    def _foreground_color(self):

        foreground_color = self.palette().color(self.foregroundRole())

        # alpha = 255
        # if self._entered:
        #     alpha -= alpha / 4
        # foreground_color.setAlpha(alpha)

        return foreground_color

    ##############################################

    def paintEvent(self, event):

        painter = QtGui.QPainter(self)

        self._draw_hover_background(painter)

        font = self.font()
        painter.setFont(font)

        text_width = self.width()
        button_height = self.height()

        foreground_color = self._foreground_color()

        # draw bullet
        painter.setPen(foreground_color)
        brush = QtGui.QBrush(QtCore.Qt.black, QtCore.Qt.SolidPattern)
        painter.setBrush(brush)
        painter.drawEllipse(QtCore.QPoint(self.__LEFT_MARGIN__/2, button_height/2),
                            self.__BULLET_RADIUS__,  self.__BULLET_RADIUS__)

        # draw text
        text_width -= self.__LEFT_MARGIN__
        rect = QtCore.QRect(self.__LEFT_MARGIN__, 0, text_width, button_height)
        flags = QtCore.Qt.AlignVCenter
        painter.drawText(rect, flags, self._label)

####################################################################################################

class DirectoryTocWidget(QtGui.QScrollArea):

    _logger = _module_logger.getChild('DirectoryTocWidget')

    path_changed = pyqtSignal(Directory)

    ##############################################

    def __init__(self, parent=None):

        super(DirectoryTocWidget, self).__init__(parent)

        self.setWidgetResizable(True)

        self._widget = QtGui.QWidget()
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self._widget.setSizePolicy(size_policy)

        self._vertical_layout = QtGui.QVBoxLayout(self._widget)
        self._vertical_layout.setSpacing(0)
        self._vertical_layout.setMargin(10)

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        metrics = QtGui.QFontMetrics(font)
        letter_width = metrics.width('W') * 2

        self._letter_widgets = {}
        self._letter_column_layouts = {}
        for letter in self.letter_iterator():
            letter_widget = QtGui.QWidget(self)
            size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
            size_policy.setVerticalStretch(0)
            letter_widget.setSizePolicy(size_policy)
            self._vertical_layout.addWidget(letter_widget)
            horizontal_layout = QtGui.QHBoxLayout(letter_widget)
            label = QtGui.QLabel(letter.upper())
            label.setFont(font)
            label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
            size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
            size_policy.setHorizontalStretch(0)
            size_policy.setVerticalStretch(0)
            size_policy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
            label.setSizePolicy(size_policy)
            label.setMinimumSize(QtCore.QSize(letter_width, 0))
            label.setMaximumSize(QtCore.QSize(letter_width, 16777215))
            horizontal_layout.addWidget(label)
            column_layout = ColumnLayout()
            horizontal_layout.addLayout(column_layout)
            self._letter_widgets[letter] = letter_widget
            self._letter_column_layouts[letter] = column_layout
            # self._vertical_layout.addStretch()

    ##############################################

    def letter_iterator(self):

        for letter in xrange(ord('a'), ord('z') +1):
            yield chr(letter)

    ##############################################

    def update(self, directory_toc):

        self._logger.info('')

        for letter in self.letter_iterator():
            letter_widget = self._letter_widgets[letter]
            letter_widget.setVisible(letter in directory_toc.letters)
            column_layout = self._letter_column_layouts[letter]
            while column_layout.count():
                widget = column_layout.takeAt(0).widget()
                widget.deleteLater()

        for letter in directory_toc.letters:
            letter_widget = self._letter_widgets[letter]
            column_layout = self._letter_column_layouts[letter]
            for directory in directory_toc[letter]:
                # button = QtGui.QPushButton(directory.basename(), parent=letter_widget)
                button = DirectoryButton(directory, parent=letter_widget)
                column_layout.addWidget(button)
                button.clicked.connect(self.path_changed)
            letter_widget.updateGeometry()

        # self._widget.updateGeometry()
        self.setWidget(self._widget)

####################################################################################################
# 
# End
# 
####################################################################################################
