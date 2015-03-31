####################################################################################################
# 
# Babel - A Bibliography Manager
# Copyright (C) Salvaire Fabrice 2015
# 
####################################################################################################

####################################################################################################

import os
import re

####################################################################################################

from .File import File

####################################################################################################

class AutomaticFileRename(object):

    """ This class implements a suffix generator to rename automatically duplicated file name.

    Example of usage::

      AutomaticFileRename('foo.py').generate()

    """
    
    ##############################################

    def __init__(self, file_path):

        """ The parameter *file_name* is the file name. """

        file_path = File(file_path)
        self._path = file_path.directory
        self._file_name, self._extension = file_path.split_extension()

    ##############################################

    def _last_cycle(self):

        """ Return the last cycle. """

        pattern = self._file_name + '-(\\d+)' + self._extension
        compiled_pattern = re.compile(pattern)
        
        cycle = 0
        for entry, match in self._path.filter_entries(compiled_pattern):
            current_cycle = int(match.groups()[0])
            cycle = max(current_cycle, cycle)

        return cycle

    ##############################################

    def _new_cycle(self):

        """ Return the next cycle. """
       
        return self._last_cycle() +1

    ##############################################

    def generate(self):

        """ Return the backup file name. """

        file_name = self._file_name + '-' + str(self._new_cycle()) + self._extension
        return self._path.join_filename(file_name)

####################################################################################################
#
# End
#
####################################################################################################
