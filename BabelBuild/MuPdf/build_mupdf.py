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

import os

####################################################################################################

from cffi import FFI
ffi = FFI()

from ctypes.util import find_library as _find_library
# from util import _find_library

####################################################################################################

mupdf_library = None

# First if there is an environment variable pointing to the library
if 'MUPDF_LIBRARY' in os.environ:
    library_path = os.path.realpath(os.environ['MUPDF_LIBRARY'])
    if os.path.exists(library_path):
        mupdf_library = library_path

# Else, try to find it
if mupdf_library is None:
    library_name = 'mupdf'
    mupdf_library = _find_library(library_name)

# Else, we failed and exit
if mupdf_library is None:
    raise OSError('MUPDF library not found')

####################################################################################################

module_path = os.path.dirname(__file__)

source = """
#include <sys/types.h>
#include <mupdf/fitz.h>

#include "fitz-extension.h"
#include "fitz-extension.c"
"""
mupdf_library_path = os.path.dirname(mupdf_library)
mupdf_include_path = os.path.join(os.path.dirname(mupdf_library_path), 'include')
freetype_include_path = '/usr/include/freetype2'
ffi.set_source('_mupdf',
                source,
                include_dirs=[mupdf_include_path, module_path, freetype_include_path],
                library_dirs=[mupdf_library_path],
                libraries=['mupdf-js-v8'])

# Parse header
source = ''
for file_name in ('mupdf-api.h', 'fitz-extension-api.h'):
    api_path = os.path.join(module_path, file_name)
    with open(api_path, 'r') as f:
        source += f.read()
ffi.cdef(source)

####################################################################################################

if __name__ == "__main__":
    ffi.compile()
