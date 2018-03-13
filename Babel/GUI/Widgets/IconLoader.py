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

""" Inspired from KIcon.
"""

####################################################################################################

import logging

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtQuick import QQuickImageProvider

from Babel.Tools.Singleton import SingletonMetaClass
import Babel.Config.ConfigInstall as ConfigInstall

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class IconLoader(metaclass=SingletonMetaClass):

    _logger = _module_logger.getChild('IconLoader')

    icon_size = 32

    ##############################################

    def __init__(self):

        self._cache = {}

    ##############################################

    def _mangle_icon_name(self, icon_name, icon_size):

        return icon_name + '@%u' % icon_size

    ##############################################

    def _demangle_icon_name(self, icon_name):

        if '@' in icon_name:
            icon_name, icon_size = icon_name.split('@')
            icon_size = int(icon_size)
        else:
            icon_size = self.icon_size

        return icon_name, icon_size

    ##############################################

    def __getitem__(self, icon_name):

        icon_name, icon_size = self._demangle_icon_name(icon_name)
        return self.get_icon(icon_name, icon_size)

    ##############################################

    def get_icon(self, icon_name, icon_size=icon_size):

        mangled_icon_name = self._mangle_icon_name(icon_name, icon_size)
        if mangled_icon_name not in self._cache:
            icon_path = str(self._find(icon_name, icon_size))
            self._cache[mangled_icon_name] = QIcon(icon_path)

        return self._cache[mangled_icon_name]

    ##############################################

    def _find(self, file_name, icon_size, extension='.png'):

        return ConfigInstall.Icon.find(file_name + extension, icon_size)

####################################################################################################

class IconProvider(QQuickImageProvider):

    _logger = _module_logger.getChild('IconProvider')

    ##############################################

    def __init__(self):

        super().__init__(QQuickImageProvider.Pixmap |
                         QQuickImageProvider.Image)

        self._icon_loader = IconLoader()

    ##############################################

    def requestImage(self, icon_name, requested_size):

        self._logger.debug('Request image {} {}'.format(icon_name, requested_size))

        raise NotImplementedError

    ##############################################

    def requestPixmap(self, icon_name, requested_size):

        # Fixme: QML cache pixmap

        self._logger.debug('Request pixmap {} {}'.format(icon_name, requested_size))

        if requested_size.isValid():
            icon = self._icon_loader.get_icon(icon_name, requested_size)
            return icon.pixmap(requested_size), requested_size
        else:
            icon = self._icon_loader[icon_name]
            size = icon.availableSizes()[0]
            return icon.pixmap(size), size
