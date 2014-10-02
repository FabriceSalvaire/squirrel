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
# 
#                                              audit 
# 
# - 08/08/2013 Fabrice
#   implement a page cache
# 
####################################################################################################

####################################################################################################

import numpy as np

import mupdf as cmupdf
from MuPDF import *

####################################################################################################

from .DocumentWords import DocumentWords
from .TextPage import TextPage
from Babel.Tools.AttributeDictionaryInterface import ReadOnlyAttributeDictionaryInterface
from Babel.Tools.Object import clone

####################################################################################################

class PdfDocument(object):

    """ This class represents a PDF Document. """

    ##############################################

    def __init__(self, path):

        self._path = path

        self._context = cmupdf.fz_new_context(None, None, cmupdf.FZ_STORE_UNLIMITED)
        encoded_path = unicode(self._path).encode('utf-8')
        self._c_document = cmupdf.fz_open_document(self._context, encoded_path)
        self._metadata = MetaData(self)
        self._number_of_pages = cmupdf.fz_count_pages(self._c_document)
        self._document_words = None

    ##############################################

    def __del__(self):

        cmupdf.fz_close_document(self._c_document)
        cmupdf.fz_free_context(self._context)

    ##############################################

    @property
    def path(self):
        return clone(self._path)

    @property
    def metadata(self):
        return self._metadata

    @property
    def number_of_pages(self):
        return self._number_of_pages

    ##############################################

    def _page(self, index):

        # Fixme: implement a cache

        return Page(self, index)

    ##############################################

    @property
    def first_page(self):
        return self._page(0)

    ##############################################

    def __getitem__(self, index):

        if isinstance(index, slice):
            return [self._page(i) for i in xrange(index.start, index.stop, index.step or 1)]
        else:
            return self._page(index)

    ##############################################

    def __iter__(self):

        for i in xrange(self._number_of_pages):
            yield self._page(i)

    ##############################################

    @property
    def words(self):

        """ Return a :obj:`.DocumentWords` instance. """

        if self._document_words is None:
            self._document_words = self._compile_document_words()

        return self._document_words

    ##############################################

    def _compile_document_words(self):

        document_words = DocumentWords()
        for page in self:
            text_page = page.text
            tokenised_text = text_page.blocks.tokenised_text
            for token in tokenised_text.word_iterator():
                document_words.add(unicode(token).lower())
        document_words.sort()

        return document_words

####################################################################################################

class MetaData(ReadOnlyAttributeDictionaryInterface):

    """ This class gives access to the PDF metadata.
    
    Public Attributes:

      :attr:`Title`

      :attr:`Subject`

      :attr:`Author`

      :attr:`Creator`

      :attr:`Producer`

      :attr:`CreationDate`

      :attr:`ModDate`

    """

    ##############################################

    def __init__(self, document):

        super(MetaData, self).__init__()

        c_document = document._c_document

        for key in (
            'Title',
            'Subject',
            'Author',
            'Creator',
            'Producer',
            'CreationDate',
            'ModDate',
            ):
            # Fixme: buffer size
            string = cmupdf.get_meta_info(c_document, key, 1024)
            if string is not None:
                # UnicodeDecodeError: 'utf8' codec can't decode byte 0x80 in position 573: invalid start byte
                try:
                    string = unicode(string, 'utf-8')
                except UnicodeDecodeError:
                    string = str(string)
            self._dictionary[key] = string

        # Fixme:
        # UnicodeDecodeError: 'utf8' codec can't decode byte 0xdb in position 2330: invalid continuation byte
        # UnicodeDecodeError: 'utf8' codec can't decode byte 0xff in position 814: invalid start byte
        fz_buffer = cmupdf.pdf_metadata(c_document)
        if False: # fz_buffer is not None:
            string = cmupdf.fz_buffer_data(fz_buffer)
            string = unicode(string, 'utf-8')
        else:
            string = None
        self._dictionary['metadata'] = string
        cmupdf.fz_drop_buffer(document._context, fz_buffer)

####################################################################################################

class Page(object):

    """ This class represents a PDF Page. Its contents could be rastered to an image or extracted as
    a text representation.
    """

    ##############################################

    def __init__(self, document, page_number):

        self._document = document
        self._context = self._document._context
        self._c_document = self._document._c_document
        self._page_number = page_number
        self._c_page = cmupdf.fz_load_page(self._c_document, page_number)
        self._text = None

    ##############################################

    @property
    def page_number(self):
        return self._page_number

    ##############################################

    def __del__(self):

        cmupdf.fz_free_page(self._c_document, self._c_page)

    ##############################################

    def _bounding_box(self):

        # Determine the size of a page at 72 dpi.
        bounds = cmupdf.fz_rect_s()
        cmupdf.fz_bound_page(self._c_document, self._c_page, bounds)

        return bounds

    ##############################################

    def _make_transform(self, scale=1, rotation=0):

        transform = cmupdf.fz_matrix_s()
        cmupdf.fz_rotate(transform, rotation)
        cmupdf.fz_pre_scale(transform, scale, scale)

        return transform

    ##############################################

    def _transform_bounding_box(self,
                                rotation=0,
                                resolution=72,
                                width=0, height=0, fit=False):

        bounds = self._bounding_box()
        scale = resolution / 72.
        transform = cmupdf.fz_matrix_s()
        cmupdf.fz_pre_scale(cmupdf.fz_rotate(transform, rotation), scale, scale)
        tmp_bounds = cmupdf.fz_rect_s()
        cmupdf.fz_copy_rect(tmp_bounds, bounds)
        ibounds = cmupdf.fz_irect_s()
        cmupdf.fz_round_rect(ibounds, cmupdf.fz_transform_rect(tmp_bounds, transform))

        # If a resolution is specified, check to see whether width/height are exceeded if not, unset them.
        if resolution != 72:
            actual_width = ibounds.x1 - ibounds.x0
            actual_height = ibounds.y1 - ibounds.y0 
            if width and actual_width <= width:
                width = 0
            if height and actual_height <= height:
                height = 0

        # Now width or height will be 0 unless they need to be enforced.
        if width or height:
            scale_x = width  / (tmp_bounds.x1 - tmp_bounds.x0)
            scale_y = height / (tmp_bounds.y1 - tmp_bounds.y0)
            if fit: # ignore aspect
                if not scale_x:
                    scale_x = 1.0 # keep computed width
                elif not scale_y:
                    scale_y = 1.0 # keep computed height
            else:
                if not scale_x:
                    scale_x = scale_y
                elif not scale_y:
                    scale_y = scale_x
                else:
                    # take the smallest scale
                    if scale_x > scale_y:
                        scale_x = scale_y
                    else:
                        scale_y = scale_x
            scale_mat = cmupdf.fz_matrix_s()
            cmupdf.fz_scale(scale_mat, scale_x, scale_y)
            cmupdf.fz_concat(transform, transform, scale_mat)
            cmupdf.fz_copy_rect(tmp_bounds, bounds)
            cmupdf.fz_transform_rect(tmp_bounds, transform)

        cmupdf.fz_round_rect(ibounds, tmp_bounds)

        return transform, ibounds

    ##############################################

    def to_png(self, path,
               rotation=0,
               resolution=72,
               width=0, height=0, fit=False,
               antialiasing_level=8,
               ):

        transform, bounding_box = self._transform_bounding_box(rotation,
                                                               resolution,
                                                               width, height, fit)
        
        pixmap = cmupdf.fz_new_pixmap_with_bbox(self._context,
                                                cmupdf.fz_device_rgb(self._context),
                                                bounding_box)
        cmupdf.fz_pixmap_set_resolution(pixmap, resolution) # purpose ?
        cmupdf.fz_clear_pixmap_with_value(self._context, pixmap, 255)

        device = cmupdf.fz_new_draw_device(self._context, pixmap)
        cmupdf.fz_set_aa_level(self._context, antialiasing_level)
        cmupdf.fz_run_page(self._c_document, self._c_page, device, transform, None)
        cmupdf.fz_write_png(self._context, pixmap, path, False)
        cmupdf.fz_free_device(device)
        cmupdf.fz_drop_pixmap(self._context, pixmap)

    ##############################################

    def to_pixmap(self,
                  rotation=0,
                  resolution=72,
                  width=None, height=None, fit=False,
                  antialiasing_level=8,
                  ):

        transform, bounding_box = self._transform_bounding_box(rotation,
                                                               resolution,
                                                               width, height, fit)
        
        width, height = rect_width_height(bounding_box)
        np_array = np.zeros((height, width, 4), dtype=np.uint8)
        pixmap = cmupdf.fz_new_pixmap_with_bbox_and_data(self._context,
                                                         cmupdf.fz_device_rgb(self._context),
                                                         bounding_box,
                                                         cmupdf.numpy_to_pixmap(np_array))
        cmupdf.fz_clear_pixmap_with_value(self._context, pixmap, 255)
        
        device = cmupdf.fz_new_draw_device(self._context, pixmap)
        cmupdf.fz_set_aa_level(self._context, antialiasing_level)
        cmupdf.fz_run_page(self._c_document, self._c_page, device, transform, None)
        cmupdf.fz_free_device(device)
        cmupdf.fz_drop_pixmap(self._context, pixmap)

        return np_array

    ##############################################

    def to_text(self, scale=1, rotation=0):

        """ Return a :obj:`.TextPage` instance. """

        transform = self._make_transform(scale, rotation)

        text_sheet = cmupdf.fz_new_text_sheet(self._context)
        text_page = cmupdf.fz_new_text_page(self._context)

        device = cmupdf.fz_new_text_device(self._context, text_sheet, text_page)
        cmupdf.fz_run_page(self._c_document, self._c_page, device, transform, None)
        cmupdf.fz_free_device(device)

        return TextPage(self, text_sheet, text_page)

    ##############################################

    @property
    def text(self):

        if self._text is None:
            self._text = self.to_text()

        return self._text

####################################################################################################
# 
# End
# 
####################################################################################################
