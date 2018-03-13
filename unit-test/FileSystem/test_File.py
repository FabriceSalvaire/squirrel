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

from Babel.FileSystem.File import *
from Babel.DataBase.FileDataBase import *

####################################################################################################

class TestFile(unittest.TestCase):

    ##############################################

    @staticmethod
    def make_file(directory, number_of_files):

        for i in range(number_of_files):
            filename = os.path.join(directory, 'file%u.pdf' % i)
            with open(filename, 'w') as f:
                f.write(str(uuid.uuid1()))

    ##############################################

    def setUp(self):

        self.tmp_directory = tempfile.mkdtemp()
        self.make_file(self.tmp_directory, number_of_files=5)
        for i in range(5):
            directory = os.path.join(self.tmp_directory, 'directory%u' % i)
            os.mkdir(directory)
            self.make_file(directory, number_of_files=5)

    ##############################################

    def test(self):

        file_database = FileDataBase(os.path.join(self.tmp_directory, 'file-database.sqlite'),
                                     echo=False)
        file_table = file_database.file_table

        directory = Directory(self.tmp_directory)
        for file_path in directory.iter_file():
            relative_file_path = file_path.relative_to(self.tmp_directory)
            print(relative_file_path, file_path.mime_type, file_path.inode, file_path.shasum)
            file_table.add(file_path)
        file_table.commit()

        print(file_table.filter_by(path=os.path.join(self.tmp_directory, 'file1.pdf')).one())

####################################################################################################

if __name__ == '__main__':

    unittest.main()
