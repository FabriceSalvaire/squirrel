####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

import os
import tempfile
import unittest
import uuid

####################################################################################################

from Babel.DataBase.WordDataBase import *

####################################################################################################

class TestWordDataBase(unittest.TestCase):

    ##############################################

    def setUp(self):

        self.tmp_directory = tempfile.mkdtemp()

    ##############################################

    def test(self):

        word_database = WordDataBase(os.path.join(self.tmp_directory, 'word-database.sqlite'),
                                     echo=True)
        language_table= word_database.language_table
        word_table = word_database.word_table

        english_language_row = LanguageRow(name='english')
        language_table.add(english_language_row)
        language_table.commit()
        print(english_language_row)

        french_language_row = LanguageRow(name='french')
        language_table.add(french_language_row)
        language_table.commit()
        print(french_language_row)
        
        word_row = WordRow(word='the', language_id=english_language_row.id, count=1)
        #word_row = WordRow(word='the', language='english', count=1)
        print(word_row)
        word_table.add(word_row)
        word_table.commit()

        word_row = WordRow(word='the', language_id=english_language_row.id, count=1)
        #word_row = WordRow(word='the', language='english', count=1)
        print(word_row)
        word_table.add(word_row)
        word_table.commit()

        word_row = WordRow(word='table', language_id=english_language_row.id, count=1)
        print(word_row)
        word_table.add(word_row)
        word_table.commit()

        word_row = WordRow(word='table', language_id=french_language_row.id, count=1)
        print(word_row)
        word_table.add(word_row)
        word_table.commit()

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
