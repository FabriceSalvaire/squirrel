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

    index = filename.rfind(os.path.extsep)
    if index == -1:
        return None
    else:
        return filename[index:]

####################################################################################################

def run_shasum(filename, algorithm=1, text=True, binary=False, portable=False):

    if algorithm not in (1, 224, 256, 384, 512, 512224, 512256):
        raise ValueError

    args = ['shasum', '--algorithm=' + str(algorithm)]
    if text:
        args.append('--text')
    if binary:
        args.append('--binary')
    if portable:
        args.append('--portable')
    args.append(filename)
    output = subprocess.check_output(args)
    shasum = output[:output.find(' ')]

    return shasum

####################################################################################################

class Path(object):

    ##############################################

    def __init__(self, path):

        self._path = os.path.abspath(path)

    ##############################################
        
    def __nonzero__(self):

        return os.path.exists(self._path) and os.path.isdir(self._path)

    ##############################################
        
    def __str__(self):

        return self._path

    ##############################################
        
    @property
    def path(self):

        return self._path

    ##############################################

    def join_directory(self, directory):

        return Path(os.path.join(self._path, directory))

    ##############################################

    def join_filename(self, filename):

        return File(filename, self._path)

    ##############################################
        
    def split(self):

        return self._path.split(os.path.sep)

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

class File(object):

    default_shasum_algorithm = 256

    ##############################################

    def __init__(self, filename, path=''):

        self._basename = os.path.basename(filename)
        if not self._basename:
            raise ValueError
        self._dirname = os.path.abspath(os.path.join(path, os.path.dirname(filename)))
        self._name = os.path.join(self._dirname, self._basename)
        self._shasum = None # lazy computation
 
    ##############################################
        
    def __nonzero__(self):

        return os.path.exists(self._name) and os.path.isfile(self._name)

    ##############################################
        
    def __str__(self):

        return self._name

    ##############################################
        
    @property
    def dirname(self):

        return self._dirname

    ##############################################
        
    @property
    def basename(self):

        return self._basename

    ##############################################
        
    @property
    def name(self):

        return self._name

    ##############################################
        
    @property
    def extension(self):

        return file_extension(self._basename)

    ##############################################
        
    @property
    def mime_type(self):

        return mimetypes.guess_type(self._basename, strict=True)

    ##############################################
        
    @property
    def inode(self):

        return os.stat(self._name).st_ino

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
        self._shasum = run_shasum(self._name, algorithm, portable=True)

        return self._shasum

####################################################################################################
# 
# End
# 
####################################################################################################
