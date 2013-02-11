####################################################################################################

import os
import tempfile
import unittest
import uuid

####################################################################################################

from Babel.FileSystem.File import *
from Babel.FileSystem.FileDataBase import *

####################################################################################################

class TestFile(unittest.TestCase):

    ##############################################

    @staticmethod
    def make_file(directory, number_of_files):

        for i in xrange(number_of_files):
            filename = os.path.join(directory, 'file%u.pdf' % i)
            with open(filename, 'w') as f:
                f.write(str(uuid.uuid1()))

    ##############################################

    def setUp(self):

        self.tmp_directory = tempfile.mkdtemp()
        self.make_file(self.tmp_directory, number_of_files=5)
        for i in xrange(5):
            directory = os.path.join(self.tmp_directory, 'directory%u' % i)
            os.mkdir(directory)
            self.make_file(directory, number_of_files=5)

    ##############################################

    def test(self):

        file_database = FileDataBase(os.path.join(self.tmp_directory, 'file-database.sqlite'),
                                     echo=False)

        directory = Directory(self.tmp_directory)
        for file_path in directory.iter_file():
            relative_file_path = file_path.relative_to(self.tmp_directory)
            print relative_file_path, file_path.mime_type, file_path.inode, file_path.shasum
            file_database.add(file_path)
        file_database.commit()

        print file_database.select_by(path=os.path.join(self.tmp_directory, 'file1.pdf')).one()

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
#
# End
#
####################################################################################################
