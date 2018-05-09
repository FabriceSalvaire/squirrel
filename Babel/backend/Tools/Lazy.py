####################################################################################################
#
# Babel - An Electronic Document Management System
# Copyright (C) 2018 Fabrice Salvaire
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

_module_logger = logging.getLogger(__name__)

####################################################################################################

class LazyInstantiator:

    _logger = _module_logger.getChild('LazyInstantiator')

    ##############################################

    def __init__(self, cls, *args, **kwargs):

        self._cls = cls
        self._args =args
        self._kwargs = kwargs
        self._instance = None

    ##############################################

    def __call__(self):

        if self._instance is None:
            self._logger.debug('Instanciate {}'.format(self._cls))
            self._instance = self._cls(*self._args, **self._kwargs)
        return self._instance
