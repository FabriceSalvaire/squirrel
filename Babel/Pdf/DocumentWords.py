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

####################################################################################################
# 
#                                              audit 
# 
# - 08/08/2013 Fabrice
#   cound or frequency
# 
####################################################################################################

####################################################################################################

class WordCount(object):

    ##############################################

    def __init__(self, word, count=1):

        self._word = unicode(word)
        self._count = count

    ##############################################

    @property
    def word(self):
        return self._word

    ##############################################

    @property
    def count(self):
        return self._count

    ##############################################

    def __cmp__(a ,b):

        return cmp(a._count, b._count)

    ##############################################

    def __unicode__(self):

        return self._word

    ##############################################

    def increment(self):

        self._count += 1

####################################################################################################

class DocumentWords(object):

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

        if not self._sorted:
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

        self._sorted_words = sorted(self._words.itervalues(), reverse=True)

####################################################################################################
# 
# End
# 
####################################################################################################
