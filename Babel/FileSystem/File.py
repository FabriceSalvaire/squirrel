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

import mimetypes
import os
import subprocess

####################################################################################################

def file_name_has_extension(file_name, extension):

    return file_name.endswith(extension)

####################################################################################################

def file_extension(filename):

    # index = filename.rfind(os.path.extsep)
    # if index == -1:
    #     return None
    # else:
    #     return filename[index:]

    return os.path.splitext(filename)[1]

####################################################################################################

def run_shasum(filename, algorithm=1, text=False, binary=False, portable=False):

    if algorithm not in (1, 224, 256, 384, 512, 512224, 512256):
        raise ValueError

    args = ['shasum', '--algorithm=' + str(algorithm)]
    if text:
        args.append('--text')
    elif binary:
        args.append('--binary')
    elif portable:
        args.append('--portable')
    args.append(filename)
    output = subprocess.check_output(args)
    shasum = output[:output.find(' ')]

    return shasum

####################################################################################################

class Path(object):

    ##############################################

    def __init__(self, path):

        self._path = str(path)

    ##############################################
        
    def __nonzero__(self):

        return os.path.exists(self._path)

    ##############################################
        
    def __str__(self):

        return self._path

    ##############################################
        
    @property
    def path(self):

        return self._path

    ##############################################

    def is_absolut(self):

        return os.path.isabs(self._path)

    ##############################################

    def absolut(self):

        return self.clone_for_path(os.path.abspath(self._path))

    ##############################################

    def normalise(self):

        return self.clone_for_path(os.path.normpath(self._path))

    ##############################################

    def normalise_case(self):

        return self.clone_for_path(os.path.normcase(self._path))

    ##############################################

    def real_path(self):

        return self.clone_for_path(os.path.realpath(self._path))

    ##############################################

    def relative_to(self, directory):

        return self.clone_for_path(os.path.relpath(self._path, str(directory)))

    ##############################################

    def join_path(self, path):

        return self.__class__(os.path.join(self._path, str(path)))

    ##############################################

    def clone_for_path(self, path):

        return self.__class__(path)

    ##############################################
        
    def split(self):

        return self._path.split(os.path.sep)

    ##############################################
        
    def split_iterator(self):

        path = Directory(os.path.sep)
        for part in self.split():
            path = path.join_directory(part)
            yield path

    ##############################################
        
    def directory_part(self):

        return Directory(os.path.dirname(self._path))

    ##############################################
        
    def basename(self):

        return os.path.basename(self._path)

    ##############################################
        
    def filename_part(self):

        # Fixme: -> basename
        return self.basename()

    ##############################################
        
    def is_directory(self):

        return os.path.isdir(self._path)

    ##############################################
        
    def is_file(self):

        return os.path.isfile(self._path)

    ##############################################
        
    def is_hidden(self):

        return self.basename().startswith('.')

    ##############################################
        
    @property
    def inode(self):

        return os.stat(self._path).st_ino

    ##############################################
        
    @property
    def creation_time(self):

        return os.stat(self._path).st_ctime

####################################################################################################

class Directory(Path):

    ##############################################
        
    def __nonzero__(self):

        return super(Directory, self).__nonzero__() and self.is_directory()

    ##############################################

    def join_directory(self, directory):

        return self.__class__(os.path.join(self._path, str(directory)))

    ##############################################

    def join_filename(self, filename):

        return File(filename, self._path)

    ##############################################

    def iter_directories(self, hidden=False):

        # Fixme: hidden directories
        for item in os.listdir(self._path):
            path = self.join_path(item)
            if path.is_directory() and (hidden or not path.is_hidden()):
                yield Directory(path)

    ##############################################

    def iter_files(self, hidden=False):

        for item in os.listdir(self._path):
            path = self.join_path(item)
            if path.is_file() and (hidden or not path.is_hidden()):
                yield File(path.filename_part(), path.directory_part())

    ##############################################

    def walk_files(self, followlinks=False):

        for root, directories, files in os.walk(self._path, followlinks=followlinks):
            for filename in files:
                yield File(filename, root)

    ##############################################

    def walk_directories(self, followlinks=False):

        for root, directories, files in os.walk(self._path, followlinks=followlinks):
            for directory in directories:
                yield Directory(os.path.join(root, directory))

####################################################################################################

class File(Path):

    default_shasum_algorithm = 256

    ##############################################

    def __init__(self, filename, path=''):

        super(File, self).__init__(os.path.join(str(path), str(filename)))

        self._filename = self.filename_part()
        if not self._filename:
            raise ValueError
        self._directory = self.directory_part()

        self._shasum = None # lazy computation
 
    ##############################################
        
    def __nonzero__(self):

        return super(File, self).__nonzero__() and os.path.isfile(self._path)

    ##############################################
        
    @property
    def directory(self):

        return self._directory

    ##############################################
        
    @property
    def filename(self):

        return self._filename

    ##############################################
        
    @property
    def extension(self):

        return file_extension(self._filename)

    ##############################################
        
    @property
    def mime_type(self):

        return mimetypes.guess_type(self._filename, strict=True)[0]

    ##############################################

    @property
    def shasum(self):

        if self._shasum is None:
            return self.compute_shasum()
        else:
            return self._shasum

    ##############################################
        
    def compute_shasum(self, algorithm=None):

        if algorithm is None:
            algorithm = self.default_shasum_algorithm
        self._shasum = run_shasum(self._path, algorithm, portable=True)

        return self._shasum

####################################################################################################
# 
# End
# 
####################################################################################################
