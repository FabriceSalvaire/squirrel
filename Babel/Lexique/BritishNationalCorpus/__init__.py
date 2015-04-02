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

from .PartOfSpeechTags import *
from Babel.Config import ConfigInstall
from Babel.DataBase.WordDataBase import WordSqliteDataBase

####################################################################################################

class BritishNationalCorpusDataBase(WordSqliteDataBase):

    ##############################################

    def __init__(self):

        database_path = ConfigInstall.WordDataBase.bnc_database_path
        super(BritishNationalCorpusDataBase, self).__init__(database_path)

        part_of_speech_tag_rows = self.part_of_speech_tag_table.all()

        self._part_of_speech_tags_by_tag = {part_of_speech_tag_row.tag:part_of_speech_tag_row
                                           for part_of_speech_tag_row in part_of_speech_tag_rows}
        self._part_of_speech_tags_by_id = {part_of_speech_tag_row.id:part_of_speech_tag_row
                                           for part_of_speech_tag_row in part_of_speech_tag_rows}
        
        self._noun_tag_ids = [self._part_of_speech_tags_by_tag[tag].id for tag in noun_tags]

    ##############################################

    def is_noun(self, word_row):

        return word_row.part_of_speech_tag_id in self._noun_tag_ids

    ##############################################

    def part_of_speech_tag_from_id(self, part_of_speech_tag_id):

        return self._part_of_speech_tags_by_id[part_of_speech_tag_id].tag

####################################################################################################
# 
# End
# 
####################################################################################################
