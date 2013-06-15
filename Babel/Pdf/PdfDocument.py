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
from Babel.Tools.DictionaryTools import DictInitialised
from Babel.Tools.Interval import IntervalInt2D
from Babel.Tools.Object import clone

####################################################################################################

def span_to_string(span):
    
    span_text = u''
    for char in TextCharIterator(span):
        span_text += unichr(char.c)
    span_text = span_text.rstrip()

    return span_text

####################################################################################################

class PdfDocument(object):

    ##############################################

    def __init__(self, path):

        self._path = path

        self._context = cmupdf.fz_new_context(None, None, cmupdf.FZ_STORE_UNLIMITED)
        self._c_document = cmupdf.fz_open_document(self._context, str(self._path))
        self._metadata = MetaData(self)
        self._number_of_pages = cmupdf.fz_count_pages(self._c_document)

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

        cmupdf.fz_close_document(self._c_document)
        cmupdf.fz_free_context(self._context)

    ##############################################

    def __getitem__(self, index):

        if isinstance(index, slice):
            return [Page(self, i) for i in xrange(index.start, index.stop, index.step or 1)]
        else:
            return Page(self, index)

    ##############################################

    def __iter__(self):

        for i in xrange(self._number_of_pages):
            yield Page(self, i)

    ##############################################

    def words(self):

        # Register words and count their occurences
        words = {}
        for page in self:
            text_page = page.to_text()
            for word in text_page.word_iterator():
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1

        words_array = sorted(words.items(), cmp=lambda a, b: cmp(a[1], b[1]), reverse=True)

        return words_array

####################################################################################################

class MetaData(ReadOnlyAttributeDictionaryInterface):

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
                string = unicode(string, 'utf-8')
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

class Page():

    ##############################################

    def __init__(self, document, page_number):

        self._document = document
        self._context = self._document._context
        self._c_document = self._document._c_document
        self._page_number = page_number
        self._c_page = cmupdf.fz_load_page(self._c_document, page_number)

    ##############################################

    @property
    def page_number(self):
        return self._page_number

    ##############################################

    def __del__(self):

        cmupdf.fz_free_page(self._c_document, self._c_page)

    ##############################################

    def _bounding_box(self):
        
        return cmupdf.fz_bound_page(self._c_document, self._c_page)

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
        cmupdf.fz_run_page(self._c_document, self._c_page, device, transform, None)
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
        cmupdf.fz_run_page(self._c_document, self._c_page, device, transform, None)
        cmupdf.fz_free_device(device)

        return PageText(self, text_sheet, text_page)

####################################################################################################

class PageText():

    ##############################################

    def __init__(self, page, text_sheet, text_page):

        self._page = page
        self._text_sheet = text_sheet
        self._text_page = text_page
        
        self._page_number = self._page._page_number
        self._document = self._page._document
        self._context = self._document._context

        self._styles = None

    ##############################################

    def __del__(self):

        cmupdf.fz_free_text_sheet(self._context, self._text_sheet)
        cmupdf.fz_free_text_page(self._context, self._text_page)

    ##############################################

    def word_iterator(self):
        
        for block in TextBlockIterator(self._text_page):
            for line in TextLineIterator(block):
                word = u''
                for span in TextSpanIterator(line):
                    for char in TextCharIterator(span):
                        unicode_char = unichr(char.c)
                        category = unicodedata.category(unicode_char)
                        # Take only letters, and numbers when it is not the first character
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
    def _to_interval(obj):

        return IntervalInt2D((obj.bbox.x0, obj.bbox.x1),
                             (obj.bbox.y0, obj.bbox.y1))

    ##############################################

    @staticmethod
    def _indent_line(text, indent_level, indent_pattern='  '):

        return indent_pattern*indent_level + text + '\n'

    ##############################################
    
    def _get_styles(self):

        styles = TextStyles()
        style = self._text_sheet.style
        while style:
            font = style.font
            styles.register_style(
                id=style.id,
                font_family=self._get_font_name(font),
                font_size=style.size,
                is_bold=bool(cmupdf.font_is_bold(font)),
                is_italic=bool(cmupdf.font_is_italic(font)),
                )
            style = style.next
        styles.sort()

        return styles

    ##############################################

    @property
    def styles(self):

        if self._styles is None:
            self._styles = self._get_styles()
        return self._styles

    ##############################################
    
    def dump_text_style(self):

        template = 'span.s%u{font-family:"%s";font-size:%gpt'
        text = ''
        style = self._text_sheet.style
        while style:
            font = style.font
            text += template % (style.id, self._get_font_name(font), style.size)
            if cmupdf.font_is_italic(font):
                text += ';font-style:italic'
            if cmupdf.font_is_bold(font):
                text += ';font-weight:bold;'
            text += '}\n'
            style = style.next

        return text

    ##############################################

    def dump_text_page_xml(self, dump_char=True):

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
                    if dump_char:
                        for char in TextCharIterator(span):
                            text += u' '*6 + '<char bbox="' + self._format_bounding_box(char) + \
                                u'" c="%s"/>\n' % (unichr(char.c))
                    else:
                        text += u' '*4 + u'<p>' + span_to_string(span) + u'</p>\n'
                    text += u' '*4 + u'</span>\n'
                text += u' '*2 + u'</line>\n'
            text += u'</block>\n'
        text += u'</page>\n'

        return text

    ##############################################

    def to_blocks(self):

        styles = self.styles
        
        blocks = TextBlocks()
        for c_block in TextBlockIterator(self._text_page):
            text_block = TextBlock(self)
            for c_line in TextLineIterator(c_block):
                line_interval = self._to_interval(c_line)
                text_line = TextLine(line_interval)
                for c_span in TextSpanIterator(c_line):
                    text_span = TextSpan(span_to_string(c_span), styles[c_span.style.id])
                    text_line.append(text_span)
                # If the line is empty then start a new block
                if not bool(text_line) and bool(text_block):
                    blocks.append(text_block)
                    text_block = TextBlock(self)
                else:
                    text_block.append(text_line)
            if bool(text_block):
                blocks.append(text_block)

        return blocks

####################################################################################################

class TextStyles(dict):

    ##############################################

    def register_style(self, **kwargs):

        style = TextStyle(**kwargs)
        self[style.id] = style
        return style

    ##############################################

    def sort(self):

        rank = 0
        current_font_size = None
        sorted_styles = sorted(self.itervalues(), reverse=True)
        for style in sorted_styles:
            # Fixme: better way?
            font_size = style.font_size
            if current_font_size is not None and font_size < current_font_size:
                rank += 1
            current_font_size = font_size
            style.rank = rank

####################################################################################################

class TextStyle(DictInitialised):

    __REQUIRED_ATTRIBUTES__ = (              
        'id',
        'font_family',
        'font_size',
        )

    __DEFAULT_ATTRIBUTES__ = dict(
        is_bold=False,
        is_italic=False,
        rank=None,
        )

    ##############################################

    def __cmp__(self, other):

        return cmp(self.font_size, other.font_size)

    ##############################################

    def __str__(self):

        template = """
Style ID %(id)u
  rank        %(rank)u
  font family %(font_family)s
  font size   %(font_size).2f
  bold        %(is_bold)s
  italic      %(is_italic)s
"""

        return template % self.__dict__

####################################################################################################

class TextStyleFrequencies(dict):

    ##############################################

    def __init__(self):

        super(TextStyleFrequencies, self).__init__()

        self._sorted_frequencies = None

    ##############################################

    def __iter__(self):

        if self._sorted_frequencies is None:
            self.sort()

        return iter(self._sorted_frequencies)

    ##############################################

    def __iadd__(self, other):

        for style_id, count in other.iteritems():
            self.fill(style_id, count)
        return self
            
    ##############################################

    def fill(self, style_id, count):

        if style_id in self:
            self[style_id] += count
        else:
            self[style_id] = count
        self._sorted_frequencies = None

    ##############################################

    def _to_list(self):

        return [TextStyleFrequency(style_id=style_id, count=count)
                for style_id, count in self.iteritems()]

    ##############################################

    def sort(self):

        self._sorted_frequencies = sorted(self._to_list(), reverse=True)

    ##############################################

    def max(self):

        if self._sorted_frequencies is None:
            self.sort()

        return self._sorted_frequencies[0]
        
####################################################################################################

class TextStyleFrequency(DictInitialised):

    __REQUIRED_ATTRIBUTES__ = (
        'style_id',
        'count',
        )

    ##############################################

    def __cmp__(self, other):

        return cmp(self.count, other.count)

####################################################################################################

class TextBlocks(list):
    pass

####################################################################################################

class TextBase(object):

    ##############################################

    def __init__(self, text=''):

        self._text = text

    ##############################################

    def __len__(self):

        return len(self._text)

    ##############################################

    def __str__(self):

        return self._text

    ##############################################

    def __unicode__(self):

        return self._text

    ##############################################

    def __nonzero__(self):

        return bool(self._text)

####################################################################################################

class TextBlock(TextBase):

    ##############################################

    def __init__(self, text_page):

        # Fixme: parent text_page versus TextBlocks

        super(TextBlock, self).__init__()

        self._text_page = text_page
        self._interval = None
        self._lines = []

    ##############################################

    @property
    def text_page(self):
        return self._text_page

    ##############################################

    @property
    def styles(self):
        return self._text_page.styles

    ##############################################

    @property
    def interval(self):
        return self._interval

    ##############################################

    @property
    def y_inf(self):
        return self._interval.y.inf

    ##############################################
        
    @property
    def number_of_styles(self):

        return sum([line.number_of_styles for line in self._lines])

    ##############################################

    def __cmp__(self, other):

        return cmp(self.y_inf, other.y_inf)

    ##############################################

    def line_iterator(self):

        return iter(self._lines)

    ##############################################

    def append(self, line):

        self._lines.append(line)
        if self._text:
            self._text += u' '
        self._text += unicode(line)
        if self._interval is not None:
            self._interval |= line.interval
        else:
            self._interval = line.interval

    ##############################################
        
    def style_frequencies(self):

        style_frequencies = TextStyleFrequencies()
        for line in self.line_iterator():
            style_frequencies += line.style_frequencies()

        return style_frequencies

####################################################################################################

class TextLine(TextBase):

    ##############################################

    def __init__(self, interval):

        super(TextLine, self).__init__()

        self._interval = interval
        self._spans = []

    ##############################################
        
    @property
    def interval(self):
        return self._interval

    ##############################################
        
    @property
    def number_of_styles(self):
        return len(self._spans)

    ##############################################
        
    def __iter__(self):
        
        return iter(self._spans)

    ##############################################

    def append(self, span):

        self._spans.append(span)
        self._text += unicode(span)

    ##############################################
        
    def style_frequencies(self):

        style_frequencies = TextStyleFrequencies()
        for span in self:
            style_id = span.style.id
            count = len(span)
            style_frequencies.fill(style_id, count)
        
        return style_frequencies

####################################################################################################

class TextSpan(TextBase):

    ##############################################

    def __init__(self, text, style):

        super(TextSpan, self).__init__(text)

        self.style = style

####################################################################################################
# 
# End
# 
####################################################################################################
