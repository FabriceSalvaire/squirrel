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

import logging

####################################################################################################

from PyQt5.QtCore import Qt, QPoint, QRect, QSize
from PyQt5.QtWidgets import QLayout

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class ColumnLayout(QLayout):

    _logger = _module_logger.getChild('ColumnLayout')

    ##############################################

    def __init__(self, parent=None, margin=10, spacing=10):

        super(ColumnLayout, self).__init__(parent)

        if parent is not None:
            # Sets the left, top, right, and bottom margins to use around the layout.
            self.setContentsMargins(margin, margin, margin, margin)
        # This property holds the spacing between widgets inside the layout.
        self.setSpacing(spacing)

        self.items = []

    ##############################################

    def __del__(self):

        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    ##############################################

    def addItem(self, item):

        self.items.append(item)

    ##############################################

    def count(self):

        return len(self.items)

    ##############################################

    def itemAt(self, index):

        # Fixme: use exception
        if index >= 0 and index < len(self.items):
            return self.items[index]
        else:
            return None

    ##############################################

    def takeAt(self, index):

        if index >= 0 and index < len(self.items):
            return self.items.pop(index)
        else:
            return None

    ##############################################

    def expandingDirections(self):

        # Returns whether this layout can make use of more space than sizeHint()
        return Qt.Orientations(Qt.Orientation(0))

    ##############################################

    def hasHeightForWidth(self):

        return True

    ##############################################

    def heightForWidth(self, width):

        height = self._compute_layout(QRect(0, 0, width, 0), True)
        # self._logger.debug('Height: {}'.format(height))
        return height

    ##############################################

    def setGeometry(self, rect):

        # self._logger.debug('rect: {} {} {} {}'.format(rect.x(), rect.y(), rect.width(), rect.height()))
        super(ColumnLayout, self).setGeometry(rect)
        self._compute_layout(rect, False)

    ##############################################

    def sizeHint(self):

        return self.minimumSize()

    ##############################################

    def minimumSize(self):

        # Return the largest "minimum size" of the items
        size = QSize()
        for item in self.items:
            size = size.expandedTo(item.minimumSize())
        margin, _, _, _ = self.getContentsMargins()
        size += QSize(2 * margin, 2 * margin)
        # self._logger.debug('size {} {}'.format(size.width(), size.height()))
        return size

    ##############################################

    def _compute_layout(self, rect, test_only):

        width = rect.width()
        maximal_width = self.minimumSize().width()
        if maximal_width:
            number_of_columns = max(width / maximal_width, 1)
        else:
            number_of_columns = 1
        if len(self) <= number_of_columns:
            number_of_lines = len(self)
            number_of_columns = 1
        else:
            number_of_lines = max(len(self) / number_of_columns, 1)
        # self._logger.debug('Maximal width {}'.format(maximal_width))
        template = '''
  Numbre of columns {}
  Numbre of items {}
  Numbre of lines {} '''
        # self._logger.debug(template.format(number_of_columns,
        #                                   len(self),
        #                                   number_of_lines))

        spacing = self.spacing()
        x = rect.x() + spacing
        y = rect.y() + spacing
        line_index = 0
        height = 0 # track the maximal height
        for item in self.items:
            # widget = item.widget()
            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            item_height = item.sizeHint().height()
            y += item_height + spacing
            height = max(height, y)
            line_index += 1
            if line_index > number_of_lines:
                line_index = 0
                x += width/number_of_columns + spacing
                y = rect.y() + spacing

        return height - rect.y()
