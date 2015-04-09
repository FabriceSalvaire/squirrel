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

"""This module implements a Python bindings for the MuPdf library using the C Foreign Function
Interface for Python.

The difference to the C API are the followings:

* The "fz_" prefix is removed.

"""

####################################################################################################

import os as _os

from cffi import FFI as _FFI

import numpy as np

####################################################################################################

from ctypes.util import find_library as _find_library
# from util import _find_library

####################################################################################################

_ffi = _FFI()
_mupdf = None

# Use a function in order to don't spoil the module
def _init():
    mupdf_library = None
    
    # First if there is an environment variable pointing to the library
    if 'MUPDF_LIBRARY' in _os.environ:
        library_path = _os.path.realpath(_os.environ['MUPDF_LIBRARY'])
        if _os.path.exists(library_path):
            mupdf_library = library_path
    
    # Else, try to find it
    if mupdf_library is None:
        library_name = 'mupdf'
        mupdf_library = _find_library(library_name)
    
    # Else, we failed and exit
    if mupdf_library is None:
        raise OSError('MUPDF library not found')

    # Parse header
    module_path = _os.path.dirname(__file__)
    source = ''
    for file_name in ('mupdf-api.h', 'fitz-extension-api.h'):
        api_path = _os.path.join(module_path, file_name)
        with open(api_path, 'r') as f:
            source += f.read()
    _ffi.cdef(source)

    global _mupdf
    # _mupdf = _ffi.dlopen(mupdf_library)
    source = """
#include <sys/types.h>
#include <mupdf/fitz.h>

#include "fitz-extension.h"
#include "fitz-extension.c"
"""
    mupdf_library_path = _os.path.dirname(mupdf_library)
    mupdf_include_path = _os.path.join(_os.path.dirname(mupdf_library_path), 'include')
    freetype_include_path = '/usr/local/stow/freetype-2.5.2/include/freetype2' # Fixme
    _mupdf = _ffi.verify(source,
                         include_dirs=[mupdf_include_path, module_path, freetype_include_path],
                         library_dirs=[mupdf_library_path],
                         libraries=['mupdf'])
    
_init()

####################################################################################################
#
# Numpy interface
#

def np_array_ptr(array):
    return _ffi.cast('void *', array.__array_interface__['data'][0])

def np_array_uint8_ptr(array):
    if array.dtype == np.uint8:
        return _ffi.cast('unsigned char *', array.__array_interface__['data'][0])
    else:
        raise ValueError("Wrong Numpy array type")

####################################################################################################
#
# String Tools
#

def decode_utf8(ptr, max_length=None):
    if ptr == _ffi.NULL:
        return ''
    else:
        if max_length is not None:
            string = _ffi.string(ptr, max_length)
        else:
            string = _ffi.string(ptr)
        try:
            return string.decode('utf-8')
        except UnicodeDecodeError:
            return str(string)
        
####################################################################################################
#
# MuPdf API
#

###################################################
#
# Structures constructors
#

def Matrix():
    return _ffi.new('fz_matrix *')

def Rect():
    return _ffi.new('fz_rect *')

def IRect():
    return _ffi.new('fz_irect *')

###################################################
#
# Constantes
#

# for convenience
NULL = _ffi.NULL # C NULL pointer

FZ_STORE_UNLIMITED = _mupdf.FZ_STORE_UNLIMITED

###################################################
#
# Functions
#

# from fitz.h

bound_page = _mupdf.fz_bound_page
clear_pixmap_with_value = _mupdf.fz_clear_pixmap_with_value
close_document = _mupdf.fz_close_document
close_output = _mupdf.fz_close_output
concat = _mupdf.fz_concat
count_pages = _mupdf.fz_count_pages
device_rgb = _mupdf.fz_device_rgb
drop_buffer = _mupdf.fz_drop_buffer
drop_pixmap = _mupdf.fz_drop_pixmap
free_context = _mupdf.fz_free_context
free_device = _mupdf.fz_free_device
free_page = _mupdf.fz_free_page
free_text_page = _mupdf.fz_free_text_page
free_text_sheet = _mupdf.fz_free_text_sheet
# new_context = _mupdf.fz_new_context
new_draw_device = _mupdf.fz_new_draw_device
new_output_with_file = _mupdf.fz_new_output_with_file
new_pixmap_with_bbox = _mupdf.fz_new_pixmap_with_bbox
new_pixmap_with_bbox_and_data = _mupdf.fz_new_pixmap_with_bbox_and_data
new_text_device = _mupdf.fz_new_text_device
new_text_page = _mupdf.fz_new_text_page
new_text_sheet = _mupdf.fz_new_text_sheet
open_document = _mupdf.fz_open_document
pixmap_set_resolution = _mupdf.fz_pixmap_set_resolution
pre_scale = _mupdf.fz_pre_scale
print_text_page = _mupdf.fz_print_text_page
print_text_page_html = _mupdf.fz_print_text_page_html
print_text_page_xml = _mupdf.fz_print_text_page_html
print_text_sheet = _mupdf.fz_print_text_sheet
rotate = _mupdf.fz_rotate
round_rect = _mupdf.fz_round_rect
run_page = _mupdf.fz_run_page
scale = _mupdf.fz_scale
set_aa_level = _mupdf.fz_set_aa_level
transform_rect = _mupdf.fz_transform_rect
write_png = _mupdf.fz_write_png

# from pdf.h
load_page = _mupdf.fz_load_page

####################################################################################################
#
# Pythonic API
#

def new_context(alloc=_ffi.NULL, locks=_ffi.NULL, max_store=_mupdf.FZ_STORE_UNLIMITED):
    return _mupdf.fz_new_context(alloc, locks, max_store)

class Context(object):
    
    ##############################################    

    def __init__(self, alloc=_ffi.NULL, locks=_ffi.NULL, max_store=_mupdf.FZ_STORE_UNLIMITED):

        self._context = _mupdf.fz_new_context(alloc, locks, max_store)

    ##############################################

    def __del__(self):

        _mupdf.fz_free_context(self._context)

###################################################

_FZ_META_INFO = 4
def get_meta_info(document, key, size=1024):
    buffer_ = _ffi.new('char[]', size) # size in bytes
    key = key.encode('utf-8')
    # key_buffer = _ffi.new('char[]', key)
    # buffer_[0] = _ffi.addressof(key_buffer, 0)
    rc = _mupdf.meta(document, _FZ_META_INFO, key, buffer_, size)
    if rc == 1:
        return decode_utf8(buffer_)
    else:
        return ''
    # raise NameError('Meta info %s not found', key)
    
####################################################################################################
#
# API extensions
#

buffer_data = _mupdf.fz_buffer_data
copy_irect = _mupdf.fz_copy_irect
copy_rect = _mupdf.fz_copy_rect
fclose = _mupdf.fz_fclose
font_is_bold = _mupdf.font_is_bold
font_is_italic = _mupdf.font_is_italic
fopen = _mupdf.fz_fopen
get_font_name = _mupdf.get_font_name
get_text_block = _mupdf.get_text_block
get_text_char = _mupdf.get_text_char
get_text_line = _mupdf.get_text_line
get_text_span = _mupdf.get_text_span
pdf_metadata = _mupdf.pdf_metadata

####################################################################################################

def rect_width_height(rect):
    return (rect.x1 - rect.x0,
            rect.y1 - rect.y0)

####################################################################################################
# 
# End
# 
####################################################################################################
