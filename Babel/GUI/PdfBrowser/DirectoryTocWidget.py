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

"""Implement a directory navigator widget rendered as table of contents.

"""

# Fixme: see DirectoryToc.qml for a QML implementation

# Notes:
#  DirectoryButton: class, obj, label

####################################################################################################

import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal

from Babel.FileSystem.File import Directory
from ..Widgets.ColumnLayout import ColumnLayout
from ..Widgets.IconLoader import IconLoader

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class DirectoryButton(QtWidgets.QPushButton):

    _logger = _module_logger.getChild('DirectoryButton')

    __BULLET_RADIUS__ = 2
    __MARGIN__ = 10
    __LEFT_MARGIN__ = 2 * (__MARGIN__ + __BULLET_RADIUS__)

    clicked = pyqtSignal(Directory)

    ##############################################

    def __init__(self, path, parent=None):

        super().__init__(parent)

        self.setFocusPolicy(Qt.TabFocus)
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
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
            # The QStyleOptionViewItem class is used to describe the parameters necessary for
            # drawing a frame.
            option = QtWidgets.QStyleOptionViewItem()
            option.initFrom(self)
            option.state = QtWidgets.QStyle.State_Enabled | QtWidgets.QStyle.State_MouseOver
            option.viewItemPosition = QtWidgets.QStyleOptionViewItem.OnlyOne
            self.style().drawPrimitive(QtWidgets.QStyle.PE_PanelItemViewItem, option, painter, self)

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

class DirectoryTocWidget(QtWidgets.QScrollArea):

    _logger = _module_logger.getChild('DirectoryTocWidget')

    path_changed = pyqtSignal(Directory)

    ##############################################

    def __init__(self, parent=None):

        super().__init__(parent)

        self._directory_toc = None

        self._init_ui()

    ##############################################

    def _init_ui(self):

        self.setWidgetResizable(True)

        self._widget = QtWidgets.QWidget()
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self._widget.setSizePolicy(size_policy)

        self._vertical_layout = QtWidgets.QVBoxLayout(self._widget)
        self._vertical_layout.setSpacing(0)
        self._vertical_layout.setContentsMargins(10, 10, 10, 10)

        icon_loader = IconLoader()
        self._go_up_button = QtWidgets.QToolButton(self)
        self._go_up_button.setIcon(icon_loader['arrow-upward-black@36'])
        self._go_up_button.setAutoRaise(True)
        self._go_up_button.clicked.connect(self._go_up)
        self._vertical_layout.addWidget(self._go_up_button)

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        metrics = QtGui.QFontMetrics(font)
        letter_width = metrics.width('W') * 2

        self._letter_widgets = {}
        self._letter_column_layouts = {}
        for letter in self.letter_iterator():
            letter_widget = QtWidgets.QWidget(self)
            size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
            size_policy.setVerticalStretch(0)
            letter_widget.setSizePolicy(size_policy)
            self._vertical_layout.addWidget(letter_widget)
            horizontal_layout = QtWidgets.QHBoxLayout(letter_widget)
            label = QtWidgets.QLabel(letter.upper())
            label.setFont(font)
            label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
            size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
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

        self._vertical_layout.addStretch(10)

    ##############################################

    def letter_iterator(self):

        for letter in range(ord('a'), ord('z') +1):
            yield chr(letter)

    ##############################################

    def update(self, directory_toc):

        # receive model

        self._logger.info('')

        self._directory_toc = directory_toc

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
                # button = QtWidgets.QPushButton(directory.basename(), parent=letter_widget)
                button = DirectoryButton(directory, parent=letter_widget)
                column_layout.addWidget(button)
                button.clicked.connect(self.path_changed)
            letter_widget.updateGeometry()

        # self._widget.updateGeometry()
        self.setWidget(self._widget)

    ##############################################

    def _go_up(self):

        # signal to model

        path = self._directory_toc.path.parent()
        self.path_changed.emit(path)
