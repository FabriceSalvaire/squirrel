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

import numpy as np

####################################################################################################

from _mupdf import ffi as _ffi
from _mupdf import lib as _lib

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

# Fixme:
FZ_STORE_UNLIMITED = _lib.FZ_STORE_UNLIMITED

###################################################
#
# Functions
#

# from fitz.h

bound_page = _lib.fz_bound_page
clear_pixmap_with_value = _lib.fz_clear_pixmap_with_value
drop_document = _lib.fz_drop_document
drop_output = _lib.fz_drop_output
concat = _lib.fz_concat
count_pages = _lib.fz_count_pages
device_rgb = _lib.fz_device_rgb
drop_buffer = _lib.fz_drop_buffer
drop_pixmap = _lib.fz_drop_pixmap
drop_context = _lib.fz_drop_context
drop_device = _lib.fz_drop_device
drop_page = _lib.fz_drop_page
#! free_text_page = _lib.fz_free_text_page
#! free_text_sheet = _lib.fz_free_text_sheet
# new_context = _lib.fz_new_context
new_draw_device = _lib.fz_new_draw_device
#! new_output_with_file = _lib.fz_new_output_with_file
new_pixmap_with_bbox = _lib.fz_new_pixmap_with_bbox
new_pixmap_with_bbox_and_data = _lib.fz_new_pixmap_with_bbox_and_data
#! new_text_device = _lib.fz_new_text_device
#! new_text_page = _lib.fz_new_text_page
#! new_text_sheet = _lib.fz_new_text_sheet
# open_document = _lib.fz_open_document
open_document = _lib.open_document
pixmap_set_resolution = _lib.fz_pixmap_set_resolution
pre_scale = _lib.fz_pre_scale
#! print_text_page = _lib.fz_print_text_page
#! print_text_page_html = _lib.fz_print_text_page_html
#! print_text_page_xml = _lib.fz_print_text_page_html
#! print_text_sheet = _lib.fz_print_text_sheet
register_document_handlers = _lib.fz_register_document_handlers
rotate = _lib.fz_rotate
round_rect = _lib.fz_round_rect
run_page = _lib.fz_run_page
scale = _lib.fz_scale
set_aa_level = _lib.fz_set_aa_level
transform_rect = _lib.fz_transform_rect
#! write_png = _lib.fz_write_png

# from pdf.h
load_page = _lib.fz_load_page

####################################################################################################
#
# Pythonic API
#

def new_context(alloc=_ffi.NULL, locks=_ffi.NULL, max_store=_lib.FZ_STORE_UNLIMITED):
    return _lib.fz_new_context(alloc, locks, max_store)

class Context(object):

    ##############################################

    def __init__(self, alloc=_ffi.NULL, locks=_ffi.NULL, max_store=_lib.FZ_STORE_UNLIMITED):

        self._context = _lib.fz_new_context(alloc, locks, max_store)

    ##############################################

    def __del__(self):

        _lib.fz_drop_context(self._context)

###################################################

def get_meta_info(ctx, document, key, size=1024):
    buffer_ = _ffi.new('char[]', size) # size in bytes
    key = key.encode('utf-8')
    # key_buffer = _ffi.new('char[]', key)
    # buffer_[0] = _ffi.addressof(key_buffer, 0)
    rc = _lib.fz_lookup_metadata(ctx, document, key, buffer_, size)
    if rc == 1:
        return decode_utf8(buffer_)
    else:
        return ''
    # raise NameError('Meta info %s not found', key)

####################################################################################################
#
# API extensions
#

buffer_data = _lib.fz_buffer_data
copy_irect = _lib.fz_copy_irect
copy_rect = _lib.fz_copy_rect
fclose = _lib.fz_fclose
font_is_bold = _lib.font_is_bold
font_is_italic = _lib.font_is_italic
fopen = _lib.fz_fopen
get_font_name = _lib.get_font_name
# get_text_block = _lib.get_text_block
# get_text_char = _lib.get_text_char
# get_text_line = _lib.get_text_line
# get_text_span = _lib.get_text_span
pdf_metadata = _lib.pdf_metadata

####################################################################################################

def rect_width_height(rect):
    return (rect.x1 - rect.x0,
            rect.y1 - rect.y0)

####################################################################################################
#
# Error Management
#

class MupdfError(NameError):
    pass

# @_ffi.callback("void(char *)")
# def throw_exit_callback(message):
#     raise MupdfError(decode_utf8(message))

# _lib.fz_set_throw_exit_callback(throw_exit_callback)

####################################################################################################
#
# End
#
####################################################################################################
