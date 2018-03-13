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

"""Implement a path navigator.

This code corresponds to a simplified translation of kdelibs/kfile/kurlnavigator.cpp to Python.

"""

# Fixme: see PathNavigator.qml for QML port

####################################################################################################

import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal

####################################################################################################

from Babel.FileSystem.File import Directory

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class PathNavigatorButton(QtWidgets.QPushButton):

    _logger = _module_logger.getChild('PathNavigatorButton')

    __BORDER_WIDTH__ = 2

    __ENTERED_HINT__ = 1
    __DRAGGED_HINT__ = 2
    __POPUP_ACTIVE_HINT__ = 4

    clicked = pyqtSignal(Directory)

    ##############################################

    def __init__(self, path, parent=None):

        super(PathNavigatorButton, self).__init__(parent)

        self._path = path
        self._label = path.basename()
        self._has_subdirectory = path.has_subdirectory()

        self.setFocusPolicy(Qt.TabFocus)
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        self.setMinimumHeight(parent.minimumHeight())

        self.setMouseTracking(True)

        self._display_hint = 0
        self._hover_arrow = False

    ##############################################

    @property
    def path(self):
        return self._path

    ##############################################

    def sizeHint(self):

        font = self.font()
        metrics = QtGui.QFontMetrics(font)
        width = metrics.width(self._label) + self._arrow_width() + 4 * self.__BORDER_WIDTH__
        # height = super(PathNavigatorButton, self).sizeHint().height()
        height = metrics.height()
        # self._logger.info("size hint {} {}".format(width, height))
        return QtCore.QSize(width, height)

    ##############################################

    def _set_display_hint_enabled(self, hint, enable):

        if enable:
            self._display_hint |= hint
        else:
            self._display_hint &= ~hint
        self.update()

    ##############################################

    def _is_display_hint_enabled(self, hint):
        return (self._display_hint & hint) > 0

    ##############################################

    def enterEvent(self, event):

        super(PathNavigatorButton, self).enterEvent(event)
        self._set_display_hint_enabled(self.__ENTERED_HINT__, True)
        self.update()

    ##############################################

    def leaveEvent(self, event):

        super(PathNavigatorButton, self).leaveEvent(event)
        self._set_display_hint_enabled(self.__ENTERED_HINT__, False)
        if self._hover_arrow:
            self._hover_arrow = False
        self.update()

    ##############################################

    def mouseMoveEvent(self, event):

        super(PathNavigatorButton, self).mouseMoveEvent(event)
        hover_arrow = self._is_above_arrow(event.x())
        if hover_arrow != self._hover_arrow:
            self._hover_arrow = hover_arrow
            self.update()

    ##############################################

    def mousePressEvent(self, event):

        if self._is_above_arrow(event.x()) and (event.button() == Qt.LeftButton):
            # the mouse is pressed above the [>] button
            self._open_sub_directories_menu()
        else:
            self.clicked.emit(self._path)
        # super(PathNavigatorButton, self).mousePressEvent(event)

    ##############################################

    def _arrow_width(self):
        return self.height() / 2

    ##############################################

    def _is_above_arrow(self, x):

        if self._has_subdirectory:
            return x >= (self.width() - self._arrow_width())
        else:
            False

    ##############################################

    def _draw_hover_background(self, painter):

        is_highlighted = (
            self._is_display_hint_enabled(self.__ENTERED_HINT__) or
            self._is_display_hint_enabled(self.__DRAGGED_HINT__) or
            self._is_display_hint_enabled(self.__POPUP_ACTIVE_HINT__)
        )

        if is_highlighted:
            # TODO: the backgroundColor should be applied to the style
            option = QtWidgets.QStyleOptionViewItem()
            option.initFrom(self)
            option.state = QtWidgets.QStyle.State_Enabled | QtWidgets.QStyle.State_MouseOver
            option.viewItemPosition = QtWidgets.QStyleOptionViewItem.OnlyOne
            self.style().drawPrimitive(QtWidgets.QStyle.PE_PanelItemViewItem, option, painter, self)

    ##############################################

    def _foreground_color(self):

        # Fixme: remove ? = foreground_color
        # Fixme: has_subdirectory = False

        is_highlighted = (
            self._is_display_hint_enabled(self.__ENTERED_HINT__) or
            self._is_display_hint_enabled(self.__DRAGGED_HINT__) or
            self._is_display_hint_enabled(self.__POPUP_ACTIVE_HINT__)
        )

        foreground_color = self.palette().color(self.foregroundRole())
        foreground_color.setAlpha(255)

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

        # draw arrow
        arrow_size = self._arrow_width()
        if self._has_subdirectory:
            arrow_x = text_width - arrow_size - self.__BORDER_WIDTH__
            arrow_y = (button_height - arrow_size) / 2
            option = QtWidgets.QStyleOption()
            option.initFrom(self)
            option.rect = QtCore.QRect(arrow_x, arrow_y, arrow_size, arrow_size)
            option.palette = self.palette()
            option.palette.setColor(QtGui.QPalette.Text, foreground_color)
            option.palette.setColor(QtGui.QPalette.WindowText, foreground_color)
            option.palette.setColor(QtGui.QPalette.ButtonText, foreground_color)

            if self._hover_arrow:
                # highlight the background of the arrow to indicate that the directories popup can be
                # opened by a mouse click
                hover_color = self.palette().color(QtGui.QPalette.HighlightedText)
                hover_color.setAlpha(96)
                painter.setPen(Qt.NoPen)
                painter.setBrush(hover_color)
                hover_x = arrow_x
                hover_x -= self.__BORDER_WIDTH__
                painter.drawRect(QtCore.QRect(hover_x, 0, arrow_size + self.__BORDER_WIDTH__, button_height))

            self.style().drawPrimitive(QtWidgets.QStyle.PE_IndicatorArrowRight, option, painter, self)

        # draw text
        painter.setPen(foreground_color)
        text_width -= arrow_size + 2 * self.__BORDER_WIDTH__
        rect = QtCore.QRect(0, 0, text_width, button_height)
        # flags = QtCore.Qt.AlignCenter
        flags = QtCore.Qt.AlignVCenter
        painter.drawText(rect, flags, self._label)

    ##############################################

    def _open_sub_directories_menu(self):

        self._set_display_hint_enabled(self.__POPUP_ACTIVE_HINT__, True)
        self.update() # ensure the button is drawn highlighted

        directories = sorted([directory.basename() for directory in self._path.iter_directories()],
                             key=lambda x: x.lower())
        if not directories:
            return

        menu = QtWidgets.QMenu(self)
        for item in directories:
            menu.addAction(item)

        popup_x = self.width() - self._arrow_width() - self.__BORDER_WIDTH__
        popup_position  = self.parentWidget().mapToGlobal(self.geometry().bottomLeft() +
                                                          QtCore.QPoint(popup_x, 0))

        action = menu.exec_(popup_position)
        if action:
            path = self._path.join_directory(action.text())
            self.clicked.emit(path)

        self._set_display_hint_enabled(self.__POPUP_ACTIVE_HINT__, False)

####################################################################################################

class PathNavigator(QtWidgets.QWidget):

    _logger = _module_logger.getChild('PathNavigator')

    path_changed = pyqtSignal(Directory)

    ##############################################

    def __init__(self, parent=None, path=None):

        super(PathNavigator, self).__init__(parent)

        self._horizontal_layout = QtWidgets.QHBoxLayout(self)
        self._horizontal_layout.setSpacing(0)
        self._horizontal_layout.setContentsMargins(0, 0, 0, 0)

        self._path = None
        if path is not None:
            self.path = path

    ##############################################

    @property
    def path(self):
        return self._path

    ##############################################

    @path.setter
    def path(self, path):
        self.set_path(path)

    ##############################################

    def set_path(self, path):
        self._set_path(path, emit=False)

    ##############################################

    def _clear_layout(self):

        layout = self._horizontal_layout
        while layout.count():
            widget = layout.takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()

    ##############################################

    def _set_path(self, path, emit=True):

        self._path = Directory(path)

        if emit:
            self.path_changed.emit(self._path)

        self._clear_layout()
        for path in self._path.split_iterator():
            widget = PathNavigatorButton(path, self)
            self._horizontal_layout.addWidget(widget)
            widget.clicked.connect(self._set_path)
        self._horizontal_layout.addStretch()
