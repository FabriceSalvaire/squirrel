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

from Babel.Config import ConfigInstall
from Babel.DataBase.CorpusDataBase import CorpusSqliteDataBase
from Babel.Tools.Singleton import SingletonMetaClass
from . import tag_registry

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class WordEntry:

    ##############################################

    def __init__(self, word_row, language):

        self._language = language
        self._word = word_row.word
        self._tags = tag_registry[language].decode_tags(*word_row.tags)
        self._frequency = word_row.frequency
        self._rank = word_row.rank
        # lemma

        self._is_noun = False
        for tag in self._tags:
            if tag.is_noun:
                self._is_noun = True

    ##############################################

    @property
    def language(self):
        return self._language

    @property
    def word(self):
        return self._word

    @property
    def tags(self):
        return self._tags

    @property
    def frequency(self):
        return self._frequency

    @property
    def rank(self):
        return self._rank

    @property
    def is_noun(self):
        return self._is_noun

    ##############################################

    def __lt__(self, other):
        return self._rank < other._rank

    ##############################################

    def __repr__(self):

        message = '''
Corpus Word Entry
  language: {0._language}
  word: {0._word}
  part of speech tags: {0._tags}
  is noun: {0.is_noun}
  rank: {0._rank}
  frequency: {0._frequency:_}
'''
        return message.format(self)

####################################################################################################

class CorpusEntry:

    ##############################################

    def __init__(self, word_row, language):

        self._languages = {}
        self._sorted_languages = None
        self.add_language(word_row, language)

    ##############################################

    def add_language(self, word_row, language):

        if language not in self._languages:
            self._languages[language] = WordEntry(word_row, language)
        else:
            raise NameError("language {} already registered for word {}".format(language, word_row.word))

    ##############################################

    @property
    def languages(self):
        return self._languages.keys()

    ##############################################

    def __len__(self):
        return len(self._languages)

    ##############################################

    def __iter__(self):
        return iter(self._languages.values())

    ##############################################

    def __getitem__(self, language):
        return self._languages[language]

    ##############################################

    @property
    def sorted_languages(self):

        if self._sorted_languages is None:
            self._sorted_languages = sorted(self._languages.values())
        return iter(self._sorted_languages)

    ##############################################

    @property
    def most_probable_language(self):
        return next(self.sorted_languages)

####################################################################################################

class CorpusRegistry(metaclass=SingletonMetaClass):

    _logger = _module_logger.getChild('CorpusRegistry')

    ##############################################

    def __init__(self):

        sqlite_path = ConfigInstall.Corpus.sqlite_path
        self._database = CorpusSqliteDataBase(sqlite_path)
        languages = ConfigInstall.Corpus.languages
        self._tables = {language:getattr(self._database, 'corpus_{}_table'.format(language))
                        for language in languages}

        self._cached_words = {}

        self._loaded = False

    ##############################################

    def load(self):

        if self._loaded:
            return

        for word_row in self._word_table.query():
            try:
                self._add(word_row)
            except RegistrationError:
                pass
        self._loaded = True

    ##############################################

    def _add(self, word_row, language):

        word = word_row.word
        # self._logger.debug('Add word "{}" for language {}'.format(word, language))
        if word_row.word in self._cached_words:
            self._cached_words[word].add_language(word_row, language)
        else:
            self._cached_words[word] = CorpusEntry(word_row, language)

    ##############################################

    def __getitem__(self, word):

        word = str(word)

        if word not in self._cached_words:
            for language, table in self._tables.items():
                word_row = table.filter_by(word=word).one_or_none()
                if word_row is not None:
                    self._add(word_row, language)

        return self._cached_words.get(word, None) # if not found
