####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

from .PartOfSpeechTags import *
from Babel.Config import ConfigInstall
from Babel.DataBase.WordDataBase import WordDataBase

####################################################################################################

class BritishNationalCorpusDataBase(WordDataBase):

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
