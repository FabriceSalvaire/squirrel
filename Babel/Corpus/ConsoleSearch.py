#! /usr/bin/env python3

####################################################################################################
#
# Babel - An Electronic Document Management System
# Copyright (C) 2017 Fabrice Salvaire
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

from Babel.Corpus.CorpusRegistry import CorpusRegistry

####################################################################################################

def console_search(args):

    word = args.query

    corpus_registry = CorpusRegistry()

    corpus_entry = corpus_registry[word]
    if corpus_entry is not None:
        print("Occurence found for word '{}'".format(word))
        for word_entry in corpus_entry.sorted_languages:
            print(word_entry)
    else:
        print("Any occurence found for word '{}'".format(word))
