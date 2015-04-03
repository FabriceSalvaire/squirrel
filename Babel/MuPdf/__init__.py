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

import os as _os

from cffi import FFI as _FFI

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
    api_path = _os.path.join(_os.path.dirname(__file__), 'mupdf-api.h')
    with open(api_path, 'r') as f:
        source = f.read()
    _ffi.cdef(source)

    global _mupdf
    _mupdf = _ffi.dlopen(mupdf_library)
            
_init()

# fz_buffer_data = _mupdf.fz_buffer_data
# fz_copy_rect = _mupdf.fz_copy_rect
# fz_load_page = _mupdf.fz_load_page

# fz_irect_s = _mupdf.fz_irect_s
# fz_matrix_s = _mupdf.fz_matrix_s
# fz_rect_s = _mupdf.fz_rect_s

# font_is_bold = _mupdf.font_is_bold
# font_is_italic = _mupdf.font_is_italic
# get_font_name = _mupdf.get_font_name
# get_meta_info = _mupdf.get_meta_info
# numpy_to_pixmap = _mupdf.numpy_to_pixmap
# pdf_metadata = _mupdf.pdf_metadata

FZ_STORE_UNLIMITED = _mupdf.FZ_STORE_UNLIMITED
fz_bound_page = _mupdf.fz_bound_page
fz_clear_pixmap_with_value = _mupdf.fz_clear_pixmap_with_value
fz_close_document = _mupdf.fz_close_document
fz_concat = _mupdf.fz_concat
fz_count_pages = _mupdf.fz_count_pages
fz_device_rgb = _mupdf.fz_device_rgb
fz_drop_buffer = _mupdf.fz_drop_buffer
fz_drop_pixmap = _mupdf.fz_drop_pixmap
fz_free_context = _mupdf.fz_free_context
fz_free_device = _mupdf.fz_free_device
fz_free_page = _mupdf.fz_free_page
fz_free_text_page = _mupdf.fz_free_text_page
fz_free_text_sheet = _mupdf.fz_free_text_sheet
fz_new_context = _mupdf.fz_new_context
fz_new_draw_device = _mupdf.fz_new_draw_device
fz_new_pixmap_with_bbox = _mupdf.fz_new_pixmap_with_bbox
fz_new_pixmap_with_bbox_and_data = _mupdf.fz_new_pixmap_with_bbox_and_data
fz_new_text_device = _mupdf.fz_new_text_device
fz_new_text_page = _mupdf.fz_new_text_page
fz_new_text_sheet = _mupdf.fz_new_text_sheet
fz_open_document = _mupdf.fz_open_document
fz_pixmap_set_resolution = _mupdf.fz_pixmap_set_resolution
fz_pre_scale = _mupdf.fz_pre_scale
fz_rotate = _mupdf.fz_rotate
fz_round_rect = _mupdf.fz_round_rect
fz_run_page = _mupdf.fz_run_page
fz_scale = _mupdf.fz_scale
fz_set_aa_level = _mupdf.fz_set_aa_level
fz_transform_rect = _mupdf.fz_transform_rect
fz_write_png = _mupdf.fz_write_png

####################################################################################################
# 
# End
# 
####################################################################################################
