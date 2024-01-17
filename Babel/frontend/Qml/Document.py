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

from PyQt5.QtCore import pyqtProperty, pyqtSignal, QObject

from Babel.backend.Corpus.LanguageId import LanguageId, language_id_to_str

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class QmlDocument(QObject):

    _logger = _module_logger.getChild('QmlDocument')

    ##############################################

    def __init__(self, row_document,  parent=None):
        super().__init__(parent)
        self._row = row_document

    ##############################################

    @property
    def row(self):
        return self._row

    ##############################################

    def commit(self):
        self._row.commit()

    ##############################################

    @pyqtProperty('QString', constant=True)
    def shasum(self):
        return self._row.shasum

    ##############################################

    has_duplicated_changed = pyqtSignal()

    @pyqtProperty('bool', notify=has_duplicated_changed)
    def has_duplicated(self):
        return self._row.has_duplicated

    ##############################################

    path_changed = pyqtSignal()

    @pyqtProperty('QString', notify=path_changed)
    def path(self):
        return str(self._row.path)

    ##############################################

    basename_changed = pyqtSignal()

    @pyqtProperty('QString', notify=basename_changed)
    def basename(self):
        return str(self._row.path.basename())

    ##############################################

    author_changed = pyqtSignal()

    @pyqtProperty('QString', notify=author_changed)
    def author(self):
        return self._row.author

    @author.setter
    def author(self, author):
        self._row.author = author
        self.commit()

    ##############################################

    language_id_changed = pyqtSignal()
    language_str_changed = pyqtSignal()

    @pyqtProperty('int', notify=language_id_changed)
    def language_id(self):
        return int(self._row.language)

    @language_id.setter
    def language_id(self, language_id):
        self._row.language = language_id
        self.commit()

    @pyqtProperty('QString', notify=language_str_changed)
    def language_str(self):
        return language_id_to_str(self._row.language)

    ##############################################

    @pyqtProperty('int', constant=True)
    def number_of_pages(self):
        return self._row.number_of_pages

    ##############################################

    title_changed = pyqtSignal()

    @pyqtProperty('QString', notify=title_changed)
    def title(self):
        return self._row.title

    @title.setter
    def title(self, title):
        self._row.title = title
        self.commit()

    ##############################################

    comment_changed = pyqtSignal()

    @pyqtProperty('QString', notify=comment_changed)
    def comment(self):
        return self._row.comment

    @comment.setter
    def comment(self, comment):
        self._row.comment = comment
        self.commit()

    ##############################################

    keywords_changed = pyqtSignal()

    @pyqtProperty('QString', notify=keywords_changed)
    def keywords(self):
        return self._row.keywords

    @keywords.setter
    def keywords(self, keywords):
        self._row.keywords = keywords
        self.commit()

    ##############################################

    star_changed = pyqtSignal()

    @pyqtProperty(int, notify=star_changed)
    def star(self):
        return self._row.star

    @star.setter
    def star(self, star):
        self._row.star = star
        self.commit()

    ##############################################

    dewey_changed = pyqtSignal()

    @pyqtProperty('QString', notify=dewey_changed)
    def dewey(self):
        return self._row.dewey

    @dewey.setter
    def dewey(self, dewey):
        self._row.dewey = dewey
        self.commit()

    ##############################################

    def __repr__(self):
        return repr(self._row)
