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

        print(file_table.select_by(path=os.path.join(self.tmp_directory, 'file1.pdf')).one())

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
