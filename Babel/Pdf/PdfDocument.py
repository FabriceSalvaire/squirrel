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

import numpy as np

import Babel.MuPdf as mupdf
from Babel.MuPdf import MupdfError

####################################################################################################

from .DocumentWords import DocumentWords
from .PdfImageCache import PdfImageCache
from .TextPage import TextPage
from Babel.Tools.AttributeDictionaryInterface import ReadOnlyAttributeDictionaryInterface
from Babel.Tools.Object import clone

####################################################################################################

class PdfDocument(object):

    """ This class represents a PDF Document. """

    ##############################################

    def __init__(self, path):

        self._path = path

        self._context = None
        self._c_document = None
        self._pages = {} # page cache

        path = str(self._path).encode('utf-8')

        # try:
        self._context = mupdf.new_context()
        mupdf.register_document_handlers(self._context)
        self._c_document = mupdf.open_document(self._context, path)
        # except MupdfError as exception:
        #     raise exception
        if self._c_document == mupdf.NULL:
            raise MupdfError()
        self._metadata = MetaData(self)
        self._number_of_pages = mupdf.count_pages(self._context, self._c_document)
        self._document_words = None
        self._image_cache = None

    ##############################################

    def __del__(self):

        # Fixme: manage properly
        for page in self._pages.values():
            page._free() # require context
        if self._c_document is not None:
            mupdf.drop_document(self._context, self._c_document)
        if self._context is not None:
            mupdf.drop_context(self._context)

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

        if not index in self._pages:
            page = Page(self, index)
            self._pages[index] = page
            return page
        else:
            return self._pages[index]

    ##############################################

    @property
    def first_page(self):
        return self._page(0)

    ##############################################

    def __getitem__(self, index):

        if isinstance(index, slice):
            return [self._page(i) for i in range(index.start, index.stop, index.step or 1)]
        else:
            return self._page(index)

    ##############################################

    def __iter__(self):

        for i in range(self._number_of_pages):
            yield self._page(i)

    ##############################################

    def iter_until(self, last_page=None):

        if last_page is None:
            last_page = self.number_of_pages -1

        for i in range(last_page +1):
            yield self._page(i)

    ##############################################

    @property
    def words(self):

        """ Return a :obj:`.DocumentWords` instance. """

        if self._document_words is None:
            self._document_words = self.collect_document_words()

        return self._document_words

    ##############################################

    def collect_document_words(self, last_page=None):

        document_words = DocumentWords()
        for page in self.iter_until(last_page):
            text_page = page.text
            tokenised_text = text_page.blocks.tokenised_text
            for token in tokenised_text.word_iterator():
                document_words.add(str(token).lower())
        document_words.sort()

        return document_words

    ##############################################

    @property
    def image_cache(self):
        if self._image_cache is None:
            self._image_cache = PdfImageCache(self)
        return self._image_cache

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
            #! string = mupdf.get_meta_info(c_document, key, size=1024)
            string = ''
            self._dictionary[key] = string

        # fz_buffer = mupdf.pdf_metadata(c_document)
        # string = mupdf.decode_utf8(mupdf.buffer_data(fz_buffer))
        string = ''
        self._dictionary['metadata'] = string
        # mupdf.drop_buffer(document._context, fz_buffer)

####################################################################################################

class Page(object):

    """ This class represents a PDF Page. Its contents could be rastered to an image or extracted as
    a text representation.
    """

    ##############################################

    def __init__(self, document, page_number): # or page_index

        self._document = document
        self._context = self._document._context
        self._c_document = self._document._c_document
        self._page_number = page_number
        self._c_page = mupdf.load_page(self._context, self._c_document, page_number)
        self._text_page = None

    ##############################################

    @property
    def page_number(self):
        return self._page_number

    ##############################################

    def _free(self):

        if self._text_page is not None:
            self._text_page._free()
        mupdf.drop_page(self._context, self._c_page)

    ##############################################

    def __del__(self):

        pass

    ##############################################

    def _bounding_box(self):

        # Determine the size of a page at 72 dpi.
        bounds = mupdf.Rect()
        mupdf.bound_page(self._context, self._c_page, bounds)

        return bounds

    ##############################################

    def _make_transform(self, scale=1, rotation=0):

        transform = mupdf.Matrix()
        mupdf.rotate(transform, rotation)
        mupdf.pre_scale(transform, scale, scale)

        return transform

    ##############################################

    def _transform_bounding_box(self,
                                rotation=0,
                                resolution=72,
                                width=0, height=0, fit=False):

        bounds = self._bounding_box()
        scale = resolution / 72.
        transform = mupdf.Matrix()
        mupdf.pre_scale(mupdf.rotate(transform, rotation), scale, scale)
        tmp_bounds = mupdf.Rect()
        mupdf.copy_rect(tmp_bounds, bounds)
        ibounds = mupdf.IRect()
        mupdf.round_rect(ibounds, mupdf.transform_rect(tmp_bounds, transform))

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
            scale_mat = mupdf.Matrix()
            mupdf.scale(scale_mat, scale_x, scale_y)
            mupdf.concat(transform, transform, scale_mat)
            mupdf.copy_rect(tmp_bounds, bounds)
            mupdf.transform_rect(tmp_bounds, transform)

        mupdf.round_rect(ibounds, tmp_bounds)

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

        pixmap = mupdf.new_pixmap_with_bbox(self._context,
                                            mupdf.device_rgb(self._context),
                                            bounding_box)
        mupdf.pixmap_set_resolution(pixmap, resolution) # purpose ?
        mupdf.clear_pixmap_with_value(self._context, pixmap, 255)

        device = mupdf.new_draw_device(self._context, pixmap)
        mupdf.set_aa_level(self._context, antialiasing_level)
        mupdf.run_page(self._context, self._c_page, device, transform, mupdf.NULL)
        path = str(path).encode('utf-8')
        # mupdf.write_png(self._context, pixmap, path, False)
        mupdf.drop_device(self._context, device)
        mupdf.drop_pixmap(self._context, pixmap)

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

        width, height = mupdf.rect_width_height(bounding_box)
        np_array = np.zeros((height, width, 4), dtype=np.uint8)
        pixmap = mupdf.new_pixmap_with_bbox_and_data(self._context,
                                                     mupdf.device_rgb(self._context),
                                                     bounding_box,
                                                     mupdf.np_array_uint8_ptr(np_array))
        mupdf.clear_pixmap_with_value(self._context, pixmap, 255)

        device = mupdf.new_draw_device(self._context, pixmap)
        mupdf.set_aa_level(self._context, antialiasing_level)
        mupdf.run_page(self._context, self._c_page, device, transform, mupdf.NULL)
        mupdf.drop_device(self._context, device)
        mupdf.drop_pixmap(self._context, pixmap)

        return np_array

    ##############################################

    def _to_text(self, scale=1, rotation=0):

        """ Return a :obj:`.TextPage` instance. """

        # Fixme: usage ?
        transform = self._make_transform(scale, rotation)

        text_sheet = mupdf.new_text_sheet(self._context)
        text_page = mupdf.new_text_page(self._context)

        device = mupdf.new_text_device(self._context, text_sheet, text_page)
        mupdf.run_page(self._context, self._c_page, device, transform, mupdf.NULL)
        mupdf.drop_device(self._context, device)

        return TextPage(self, text_sheet, text_page)

    ##############################################

    @property
    def text(self):

        if self._text_page is None:
            self._text_page = self._to_text()
        return self._text_page
