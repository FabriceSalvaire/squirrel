####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

import unicodedata

import numpy as np

import mupdf as cmupdf
from MuPDF import *

####################################################################################################

from Babel.Tools.AttributeDictionaryInterface import ReadOnlyAttributeDictionaryInterface
from Babel.Tools.Object import clone

####################################################################################################

class PdfDocument(object):

    ##############################################

    def __init__(self, path):

        self._path = path

        self._context = cmupdf.fz_new_context(None, None, cmupdf.FZ_STORE_UNLIMITED)
        self._document = cmupdf.fz_open_document(self._context, str(self._path))
        self._metadata = PdfMetaData(self)
        self._number_of_pages = cmupdf.fz_count_pages(self._document)

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

    def __del__(self):

        cmupdf.fz_close_document(self._document)
        cmupdf.fz_free_context(self._context)

    ##############################################

    def __getitem__(self, index):

        if isinstance(index, slice):
            return [PdfPage(self, i) for i in xrange(index.start, index.stop, index.step)]
        else:
            return PdfPage(self, index)

    ##############################################

    def __iter__(self):

        for i in xrange(self._number_of_pages):
            yield PdfPage(self, i)

    ##############################################

    def words(self):

        words = {}
        for pdf_page in self:
            pdf_text_page = pdf_page.to_text()
            for word in pdf_text_page.word_iterator():
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1

        words_array = sorted(words.items(), cmp=lambda a, b: cmp(a[1], b[1]), reverse=True)

        return words_array

####################################################################################################

class PdfMetaData(ReadOnlyAttributeDictionaryInterface):

    ##############################################

    def __init__(self, pdf_document):

        super(PdfMetaData, self).__init__()

        document = pdf_document._document

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
            self._dictionary[key] = unicode(cmupdf.get_meta_info(document, key, 1024), 'utf-8')

        fz_buffer = cmupdf.pdf_metadata(document)
        # Fixme: UnicodeDecodeError: 'utf8' codec can't decode byte 0xdb in position 2330: invalid
        #   continuation byte
        string = cmupdf.fz_buffer_data(fz_buffer)
        self._dictionary['metadata'] = unicode(string, 'utf-8')
        cmupdf.fz_drop_buffer(pdf_document._context, fz_buffer)

####################################################################################################

class PdfPage():

    ##############################################

    def __init__(self, pdf_document, page_number):

        self._pdf_document = pdf_document
        self._context = self._pdf_document._context
        self._document = self._pdf_document._document
        self._page_number = page_number
        self._page = cmupdf.fz_load_page(self._document, page_number)

    ##############################################

    @property
    def page_number(self):
        return self._page_number

    ##############################################

    def __del__(self):

        cmupdf.fz_free_page(self._document, self._page)

    ##############################################

    def _bounding_box(self):
        
        return cmupdf.fz_bound_page(self._document, self._page)

    ##############################################

    def _make_transform(self, scale=1, rotation=0):

        transform = cmupdf.fz_scale(scale, scale)
        transform = cmupdf.fz_concat(transform, cmupdf.fz_rotate(rotation))

        return transform

    ##############################################

    def _transform_bounding_box(self, transform):

        bounding_box = self._bounding_box()
        bounding_box = cmupdf.fz_transform_rect(transform, bounding_box)

        return bounding_box

    ##############################################

    def to_pixmap(self, scale=1, rotation=0, antialiasing_level=8):

        transform = self._make_transform(scale, rotation)
        bounding_box = self._transform_bounding_box(transform)
        bounding_box = cmupdf.fz_round_rect(bounding_box)

        width, height = rect_width_height(bounding_box)
        np_array = np.zeros((height, width, 4), dtype=np.uint8)
        pixmap = cmupdf.fz_new_pixmap_with_bbox_and_data(self._context,
                                                         cmupdf.get_fz_device_rgb(),
                                                         bounding_box,
                                                         cmupdf.numpy_to_pixmap(np_array))
        cmupdf.fz_clear_pixmap_with_value(self._context, pixmap, 0xff)
        
        device = cmupdf.fz_new_draw_device(self._context, pixmap)
        cmupdf.fz_set_aa_level(self._context, antialiasing_level)
        cmupdf.fz_run_page(self._document, self._page, device, transform, None)
        cmupdf.fz_free_device(device)
        cmupdf.fz_drop_pixmap(self._context, pixmap)

        return np_array

    ##############################################

    def to_text(self, scale=1, rotation=0):

        transform = self._make_transform(scale, rotation)
        bounding_box = self._transform_bounding_box(transform)

        text_sheet = cmupdf.fz_new_text_sheet(self._context)
        text_page = cmupdf.fz_new_text_page(self._context, bounding_box)

        device = cmupdf.fz_new_text_device(self._context, text_sheet, text_page)
        cmupdf.fz_run_page(self._document, self._page, device, transform, None)
        cmupdf.fz_free_device(device)

        return PdfTextPage(self, text_sheet, text_page)

####################################################################################################

class PdfTextPage():

    ##############################################

    def __init__(self, pdf_page, text_sheet, text_page):

        self._pdf_page = pdf_page
        self._text_sheet = text_sheet
        self._text_page = text_page
        
        self._page_number = self._pdf_page._page_number
        self._pdf_document = self._pdf_page._pdf_document
        self._context = self._pdf_document._context

    ##############################################

    def __del__(self):

        cmupdf.fz_free_text_sheet(self._context, self._text_sheet)
        cmupdf.fz_free_text_page(self._context, self._text_page)

    ##############################################

    def word_iterator(self):

        word = 'u'
        for block in TextBlockIterator(self._text_page):
            for line in TextLineIterator(block):
                for span in TextSpanIterator(line):
                    for char in TextCharIterator(span):
                        unicode_char = unichr(char.c)
                        category = unicodedata.category(unicode_char)
                        # Take only letters, and numbers when it is not the first character
                        print unicode_char, category, word
                        if ((category in ('Ll', 'Lu')) or (category == 'Nd' and word)):
                            word += unicode_char.lower()
                        elif word:
                            yield word
                            word = u''
            if word: # Last char was a letter/number
                yield word

    ##############################################

    @staticmethod
    def _get_font_name(font):

        font_name = cmupdf.get_font_name(font)
        i = font_name.find('+')
        if i:
            font_name = font_name[i+1:] 

        return font_name

    ##############################################

    @staticmethod
    def _format_bounding_box(obj):

        return "[%g %g %g %g]" % (obj.bbox.x0, obj.bbox.y0,
                                  obj.bbox.x1, obj.bbox.y1)

    ##############################################

    @staticmethod
    def _indent_line(text, indent_level, indent_pattern='  '):

        return indent_pattern*indent_level + text + '\n'

    ##############################################
    
    def dump_text_style(self):

        template = 'span.s%u{font-family:"%s";font-size:%gpt'
        text = ''
        style = self._text_sheet.style
        while style:
            font = style.font
            text = template % (style.id, self._get_font_name(font), style.size)
            if cmupdf.font_is_italic(font):
                text += ';font-style:italic'
            if cmupdf.font_is_bold(font):
                text += ';font-weight:bold;'
            text += '}\n'
            style = style.next

        return text

    ##############################################

    def dump_text_page_xml(self):

        text = u'<page page_number="%u">\n' % (self._page_number)
        for block in TextBlockIterator(self._text_page):
            text += u'<block bbox="' + self._format_bounding_box(block) + u'">\n'
            for line in TextLineIterator(block):
                text += u' '*2 + u'<line bbox="' + self._format_bounding_box(line) + u'">\n'
                for span in TextSpanIterator(line):
                    style = span.style
                    font_name = self._get_font_name(style.font)
                    text += u' '*4 + u'<span bbox="' + self._format_bounding_box(span) + \
                        u'" font="%s" size="%g">\n' % (font_name, style.size)
                    for char in TextCharIterator(span):
                        text += u' '*6 + u'<char bbox="' + self._format_bounding_box(char) + \
                            u'" c="%s"/>\n' % (unichr(char.c))
                    text += u' '*4 + u'</span>\n'
                text += u' '*2 + u'</line>\n'
            text += u'</block>\n'
        text += u'</page>\n'

        return text

    ##############################################

    def dump_text_page(self):

        text = u''
        empty_block = False
        for block in TextBlockIterator(self._text_page):
            if not empty_block:
                text += u'\n'
            empty_block = True
            for line in TextLineIterator(block):
                line_text = u''
                for span in TextSpanIterator(line):
                    span_text = u''
                    for char in TextCharIterator(span):
                        span_text += unichr(char.c)
                    span_text = span_text.rstrip()
                    if span_text:
                        line_text += span_text
                if line_text:
                    text += line_text + u'\n'
                    empty_block = False
        
        return text

    ##############################################

    def block_iterator(self):
        
        for block in TextBlockIterator(self._text_page):
            block_text = u''
            for line in TextLineIterator(block):
                line_text = u''
                for span in TextSpanIterator(line):
                    span_text = u''
                    for char in TextCharIterator(span):
                        span_text += unichr(char.c)
                    span_text = span_text.rstrip()
                    if span_text: # Append span to line
                        line_text += span_text
                    else: # Empty span then append a block
                        if block_text:
                            yield block_text
                        block_text = u''
                        line_text = u''
                # Append line to block
                if block_text:
                    block_text += ' '
                block_text += line_text
            if block_text:
                yield block_text

####################################################################################################
# 
# End
# 
####################################################################################################
