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

from .PartOfSpeechTags import noun_tags
from Babel.Config import ConfigInstall
from Babel.DataBase.WordDataBase import WordSqliteDataBase

####################################################################################################

class BritishNationalCorpusDataBase(WordSqliteDataBase):

    ##############################################

    def __init__(self):

        database_path = ConfigInstall.WordDataBase.bnc_database_path
        super(BritishNationalCorpusDataBase, self).__init__(database_path)

####################################################################################################

class Tag(object):

    ##############################################

    def __init__(self, tag_id, tag):

        self.id = tag_id
        self.tag = tag
        self.is_noun = tag in noun_tags

    ##############################################

    def __repr__(self):
        return self.tag
    
####################################################################################################

class TaggedWord(object):

    ##############################################
    
    def __init__(self, word, tag):

        self.word = word
        self.tag = tag
        self.is_noun = tag.is_noun

    ##############################################

    def __repr__(self):
        return self.word

####################################################################################################

class RegistrationError(NameError):
    pass

####################################################################################################

class TaggedWords(dict):

    ##############################################

    def __init__(self):

        super(TaggedWords, self).__init__()
        
        self.is_noun = False
        
    ##############################################

    def add(self, tagged_word):

        if tagged_word.tag not in self:
            self[tagged_word.tag] = tagged_word
            self.is_noun |= tagged_word.is_noun
        else:
            raise RegistrationError("TaggedWord is already registered")
        
####################################################################################################

class BritishNationalCorpus(object):

    ##############################################

    def __init__(self):

        self._database = BritishNationalCorpusDataBase()
        self._word_table = self._database.word_table
        
        self._cached_words = {}

        self._tags = {}
        for tag_row in  self._database.part_of_speech_tag_table.query():
            tag = Tag(tag_row.id, tag_row.tag)
            self._tags[tag.id] = tag
            self._tags[tag.tag] = tag

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
        
    def _add(self, word_row):

        word = word_row.word
        tag = self._tags[word_row.part_of_speech_tag_id]
        tagged_word = TaggedWord(word, tag)
        if word not in self._cached_words:
            self._cached_words[word] = tagged_words = TaggedWords()
        else:
            tagged_words = self._cached_words[word]
        tagged_words.add(tagged_word)
            
    ##############################################

    def __getitem__(self, word):

        if word not in self._cached_words:
            query = list(self._word_table.filter_by(word=word))
            if len(query): # Fixme: better ?
                for word_row in query:
                    self._add(word_row)
            else:
                return None
        return self._cached_words[word]
        
####################################################################################################
# 
# End
# 
####################################################################################################
