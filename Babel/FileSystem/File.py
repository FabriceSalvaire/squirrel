####################################################################################################
# 
# Babel - 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

import mimetypes
import os
import subprocess

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

    def clone_for_path(self, path):

        return self.__class__(path)

    ##############################################
        
    def split(self):

        return self._path.split(os.path.sep)

    ##############################################
        
    def directory_part(self):

        return Directory(os.path.dirname(self._path))

    ##############################################
        
    def filename_part(self):

        return os.path.basename(self._path)

    ##############################################
        
    def is_directory(self):

        return os.path.isdir(self._path)

    ##############################################
        
    def is_file(self):

        return os.path.isfile(self._path)

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

    def iter_file(self, followlinks=False):

        for root, directories, files in os.walk(self._path, followlinks=followlinks):
            for filename in files:
                yield File(filename, root)

    ##############################################

    def iter_directories(self, followlinks=False):

        for root, directories, files in os.walk(self._path, followlinks=followlinks):
            for directory in directories:
                yield Path(os.path.join(root, directory))

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
