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

from .LanguageId import LanguageId

####################################################################################################

class WordCount:

    __corpus_registry__ = None # lazy local cache for singleton

    ##############################################

    def __init__(self, word, count=1):

        self._word = str(word)
        self._count = count
        self._rank = None

        self._resolved = False
        self._corpus_entry = None
        self._word_entry = None

    ##############################################

    @property
    def word(self):
        return self._word

    @property
    def count(self):
        return self._count

    @property
    def rank(self):
        return self._rank

    ##############################################

    def __lt__(a ,b):

        return a._count < b._count

    ##############################################

    def __str__(self):

        return self._word

    ##############################################

    def increment(self):

        self._count += 1

    ##############################################

    def _resolve(self):

        if not self._resolved:

            if self.__corpus_registry__ is None:
                from .CorpusRegistry import CorpusRegistry
                self.__corpus_registry__ = CorpusRegistry()

            self._corpus_entry = self.__corpus_registry__[self._word]

            if self._corpus_entry is not None:
                self._word_entry = self._corpus_entry.most_probable_language

            self._resolved = True

    ##############################################

    @property
    def corpus_entry(self):
        self._resolve()
        return self._corpus_entry

    @property
    def word_entry(self):
        self._resolve()
        return self._word_entry

####################################################################################################

class DocumentWords:

    ##############################################

    def __init__(self):

        self._words = {}

        self._sorted_words = []
        self._sorted = False

    ##############################################

    def __len__(self):
        return len(self._words)

    ##############################################

    def __iter__(self):
        self.sort()
        return iter(self._sorted_words)

    ##############################################

    def add(self, word):

        """ Register the word and count its occurence. """

        words = self._words
        if word in words:
            words[word].increment()
        else:
            words[word] = WordCount(word)

        self._sorted = False

    ##############################################

    def sort(self):

        """ Sort the word by frequency in descending order. """

        if not self._sorted:
            self._sorted_words = sorted(iter(self._words.values()), reverse=True)
            for rank, word_count in enumerate(self._sorted_words):
                word_count._rank = rank
            self._sorted = True

    ##############################################

    def language_count(self):

        languages = {language:0 for language in LanguageId._member_names_} # Fixme: private API
        for word_count in self:
            word_entry = word_count.word_entry
            if word_entry is None:
                language = 'unknown'
            else:
                language = word_count.word_entry.language
            languages[language] += word_count.count
        return languages

    ##############################################

    def dominant_language(self):

        sorted_languages = sorted(list(self.language_count().items()), key=lambda x: x[1])
        language, count = sorted_languages[-1]
        if count:
            return language
        else:
            return None
