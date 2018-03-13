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
