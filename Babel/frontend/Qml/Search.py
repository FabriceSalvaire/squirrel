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

from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtQml import QQmlListProperty

from Babel.backend.Search import Searcher
from .Document import QmlDocument

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class QmlSearchManager(QObject):

    _logger = _module_logger.getChild('QmlSearchManager')

    ##############################################

    def __init__(self, application): # , parent=None
        super().__init__(application)
        self._application = application
        self._searcher = Searcher(application)
        self._results = []
        self._query = ''

    ##############################################

    def __len__(self):
        return len(self._results)

    def __iter__(self):
        return iter(self._results)

    def __getitem__(self, slice_):
        return self._results[slice_]

    ##############################################

    results_changed = pyqtSignal()

    @pyqtProperty(QQmlListProperty, notify=results_changed)
    def results(self):
        return QQmlListProperty(QmlDocument, self, self._results)
    # append=

    ##############################################

    @pyqtSlot()
    def clear(self):
        self._results.clear()
        self.results_changed.emit()

    ##############################################

    # @pyqtSlot('QString')
    # def search(self, query):

    query_changed = pyqtSignal()

    @pyqtProperty('QString', notify=query_changed) # ???
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._logger.debug('Update query:{}'.format(query))
        self._query = query
        self._results = [QmlDocument(row) for row in self._searcher.search_in_word_table(query)]
        self._logger.debug('found {} documents'.format(len(self._results)))
        self.results_changed.emit()
