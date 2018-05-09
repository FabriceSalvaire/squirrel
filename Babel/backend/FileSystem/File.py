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

import mimetypes
import os

from .Shasum import shasum
from .UserXattr import UserXattr

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

class Path:

    # Fixme: versus pathlib

    ##############################################

    def __init__(self, path):
        self._path = str(path)

    ##############################################

    def __repr__(self):
        return 'Path ' + self._path

    ##############################################

    def __bool__(self):
        return self.exists()

    ##############################################

    def exists(self):
        return os.path.exists(self._path)

    ##############################################

    def __eq__(self, other):
        return self._path == str(other)

    ##############################################

    def __ne__(self, other):
        return self._path != str(other)

    ##############################################

    def __str__(self):
        return self._path

    @property
    def path(self):
        # Fixme: purpose ???
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

    def is_relative_to(self, directory):
        return str(self).startswith(str(directory))

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
        """ Return ['', 'a', 'b', 'c'] for '/a/b/c' """
        # Fixme: remove ''?
        return self._path.split(os.path.sep)

    ##############################################

    def split_iterator(self):

        """ Return [Path /, Path /a, Path /a/b, Path /a/b/c] for '/a/b/c' """

        # Fixme: name ?

        path = Directory(os.path.sep)
        for directory in self.split():
            path = path.join_directory(directory)
            yield path

    ##############################################

    def split_reverse_iterator(self):

        for directory in reversed(self.split()):
            if directory:
                yield directory

    ##############################################

    def reverse_level_of_equality(self, other):

        """ Return the level of subdirectory from the top matching both paths. """

        level = 0
        for directory1, directory2 in zip(self.split_reverse_iterator(),
                                          other.split_reverse_iterator()):
            if directory1 != directory2:
                break
            else:
                level += 1
        return level

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

    # alias
    parent = Path.directory_part

    ##############################################

    def __bool__(self):
         # Fixme: right ?
        return self.exists() and self.is_directory()

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

    def has_subdirectory(self, hidden=False):

        # Fixme: hidden directories
        for item in os.listdir(self._path):
            path = self.join_path(item)
            if path.is_directory() and (hidden or not path.is_hidden()):
                return True

    ##############################################

    def iter_files(self, hidden=False):

        for item in os.listdir(self._path):
            path = self.join_path(item)
            if path.is_file() and (hidden or not path.is_hidden()):
                yield File(path.filename_part(), path.directory_part())

    ##############################################

    def filter_entries(self, compiled_pattern):

        for item in os.listdir(str(self._path)):
            match = compiled_pattern.match(item)
            if match is not None:
                yield item, match

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

    default_shasum_algorithm = 1 # 256

    ##############################################

    def __init__(self, filename, path=''):

        super(File, self).__init__(os.path.join(str(path), str(filename)))

        self._filename = self.filename_part()
        if not self._filename:
            raise ValueError
        self._directory = self.directory_part()

        # lazy
        self._shasum = None
        self._xattr = None

    ##############################################

    def __bool__(self):
        # Fixme: right ?
        return self.exists() and os.path.isfile(self._path)

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

    def split_extension(self):
        return os.path.splitext(self._filename)

    ##############################################

    @property
    def mime_type(self):
        return mimetypes.guess_type(self._filename, strict=True)[0]

    ##############################################

    @property
    def shasum(self):

        # Fixme: check file don't change, modification date ?
        if self._shasum is None:
            return self.compute_shasum()
        else:
            return self._shasum

    ##############################################

    def compute_shasum(self, algorithm=None):

        if algorithm is None:
            algorithm = self.default_shasum_algorithm
        # self._shasum = run_shasum(self._path, algorithm, binary=True)
        self._shasum = shasum(self._path, algorithm)

        return self._shasum

    ##############################################

    @property
    def xattr(self):

        # Fixme: api

        if self._xattr is None:
            self._xattr = UserXattr(self._path)
        return self._xattr

    ##############################################

    def delete(self):
        os.unlink(self._path)

    ##############################################

    @property
    def size(self):
        return os.stat(self._path).st_size
