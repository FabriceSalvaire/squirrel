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

import Babel.MuPdf as mupdf
import Babel.MuPdf.TextIterator as mupdf_iter

####################################################################################################

from .MupdfTools import *
from .TextStyle import TextStyles, TextStyleFrequencies
from Babel.Pdf.TextTokenizer import TextTokenizer, TokenisedText
from Babel.Math.Interval import IntervalInt2D

####################################################################################################

class TextPage():

    """ This class represents the textual content of a page. """

    ##############################################

    def __init__(self, page, text_sheet, text_page):

        self._page = page
        self._text_sheet = text_sheet
        self._text_page = text_page
        
        self._page_number = self._page._page_number
        self._document = self._page._document
        self._context = self._document._context

        self._styles = None
        self._blocks = None

    ##############################################

    def _free(self):

        # text_sheet and text_page was not created in TextPage
        mupdf.free_text_sheet(self._context, self._text_sheet)
        mupdf.free_text_page(self._context, self._text_page)
        
    ##############################################

    def __del__(self):

        pass

    ##############################################

    @property
    def page_number(self):
        return self._page_number

    ##############################################

    @property
    def interval(self):
        return to_interval(self._text_page.mediabox)

    ##############################################
    
    def _get_styles(self):

        """ Return an :obj:`.TextStyles` instance for the styles of the page. """

        styles = TextStyles()
        style = self._text_sheet.style
        while style:
            styles.register_style(to_text_style(style))
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

    def _append_span_text(self, text_line, span_text, style_id):

        span_text = span_text.rstrip()
        text_span = TextSpan(span_text, self.styles[style_id])
        text_line.append(text_span)

    ##############################################

    def _get_blocks(self):

        """ Return an :obj:`TextBlocks` instance for the page. """

        blocks = TextBlocks()
        for c_block in mupdf_iter.TextBlockIterator(self._text_page):
            text_block = TextBlock(self)
            for c_line in mupdf_iter.TextLineIterator(c_block):
                line_interval = to_interval(c_line.bbox)
                text_line = TextLine(line_interval)
                for c_span in mupdf_iter.TextSpanIterator(c_line):
                    style_id = None
                    span_text = ''
                    for c_char in mupdf_iter.TextCharIterator(c_span):
                        # Fixme: Style addresses are alternated. Why?
                        char_style_id = c_char.style.id
                        char = chr(c_char.c)
                        if char_style_id is not style_id:
                            if span_text:
                                self._append_span_text(text_line, span_text, style_id)
                            style_id = char_style_id
                            span_text = char
                        else:
                            span_text += char
                    if span_text:
                        self._append_span_text(text_line, span_text, style_id)
               # If the line is empty then start a new block
                if not bool(text_line) and bool(text_block):
                    blocks.append(text_block)
                    text_block = TextBlock(self)
                else:
                    text_block.append(text_line)
            if bool(text_block):
                blocks.append(text_block)

        blocks.sort()

        return blocks

    ##############################################

    @property
    def blocks(self):

        if self._blocks is None:
            self._blocks = self._get_blocks()
        return self._blocks

    ##############################################
    
    def dump_text_style(self):

        # Fixme: old and historical code, move elsewhere ?

        template = 'span.s%u{font-family:"%s";font-size:%gpt'
        text = ''
        style = self._text_sheet.style
        while style:
            font = style.font
            text += template % (style.id, get_font_name(font), style.size)
            if mupdf.font_is_italic(font):
                text += ';font-style:italic'
            if mupdf.font_is_bold(font):
                text += ';font-weight:bold;'
            text += '}\n'
            style = style.__next__

        return text

    ##############################################

    def dump_text_page_xml(self, dump_char=True):

        # Fixme: old and historical code, move elsewhere ?

        text = '<page page_number="%u">\n' % (self._page_number)
        for block in mupdf_iter.TextBlockIterator(self._text_page):
            text += '<block bbox="' + format_bounding_box(block) + '">\n'
            for line in mupdf_iter.TextLineIterator(block):
                text += ' '*2 + '<line bbox="' + format_bounding_box(line) + '">\n'
                for span in mupdf_iter.TextSpanIterator(line):
                    style_id = None
                    if dump_char:
                        for char in mupdf_iter.TextCharIterator(span):
                            # Fixme: Style addresses are alternated. Why?
                            if char.style.id is not style_id:
                                if style_id is not None:
                                    text += ' '*4 + '</span>\n'
                                style = char.style
                                style_id = style.id
                                font_name = get_font_name(style.font)
                                # Fixme: bounding box is wrong
                                text += ' '*4 + '<span bbox="' + format_bounding_box(span) + \
                                    '" font="%s" size="%g">\n' % (font_name, style.size)
                            text += ' '*6 + '<char c="%s"/>\n' % (chr(char.c))
                        if style_id is not None:
                            text += ' '*4 + '</span>\n'
                    else:
                        text += ' '*4 + '<p>' + span_to_string(span) + '</p>\n'
                text += ' '*2 + '</line>\n'
            text += '</block>\n'
        text += '</page>\n'

        return text

####################################################################################################

class TextBlocks(object):

    """ This class implements a list of text blocks. """

    ##############################################

    def __init__(self):

        self._blocks = []
        self._sorted_blocks = None
        self._tokenised_text = None

    ##############################################

    def __bool__(self):
        
        return bool(self._blocks)

    ##############################################

    def __len__(self):
        
        return len(self._blocks)

    ##############################################

    def __iter__(self):
        
        return iter(self._blocks)

    ##############################################

    def sorted_iter(self):
        
        return iter(self._sorted_blocks)

    ##############################################

    def __getitem__(self, index):

        return self._blocks[index]

    ##############################################

    def append(self, text_block):
        
        self._blocks.append(text_block)
        text_block.block_id = len(self._blocks) -1
        self._sorted_blocks = None

    ##############################################

    def sort(self):

        """ Sort the block by y in ascending order. """
        
        self._sorted_blocks = sorted(self._blocks)
        y_rank = 0
        y = None
        for text_block in self._sorted_blocks:
            if y is None:
                y = text_block.y_inf
            elif y < text_block.y_inf:
                y_rank += 1
            text_block.y_rank = y_rank

    ##############################################

    @property
    def tokenised_text(self):

        """ Return an instance of :obj:`TokenisedText`. """
        
        if self._tokenised_text is None:
            self._tokenised_text = TokenisedText()
            for block in self:
                self._tokenised_text += block.tokenised_text

        return self._tokenised_text

####################################################################################################

class TextBase(object):

    ##############################################

    def __init__(self, text=''):

        self._text = text
        self._tokenised_text = None

    ##############################################

    def __len__(self):

        return len(self._text)

    ##############################################

    def __str__(self):

        return self._text

    ##############################################

    def __bool__(self):

        return bool(self._text)

    ##############################################

    @property
    def tokenised_text(self):
        
        if self._tokenised_text is None:
            self._tokenised_text = TextTokenizer().lex(str(self._text))

        return self._tokenised_text

####################################################################################################

class TextBlock(TextBase):

    # block id page/index X
    # text X
    # styles X
    # main_style X
    # length X
    # interval X
    # is centred
    # y rank
    # user tag

    ##############################################

    def __init__(self, text_page):

        # Fixme: parent text_page versus TextBlocks

        super(TextBlock, self).__init__()

        self._block_id = None
        self._y_rank = None
        self._text_page = text_page
        self._interval = None
        self._lines = []
        self._style_frequencies = None

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
    def block_id(self):
        return self._block_id

    ##############################################

    @block_id.setter
    def block_id(self, block_id):
        self._block_id = block_id

    ##############################################

    @property
    def interval(self):
        return self._interval

    ##############################################

    @property
    def horizontal_margin(self):

        return (self._interval.x.inf - self.text_page.interval.x.inf,
                self.text_page.interval.x.sup - self._interval.x.sup)

    ##############################################

    @property
    def is_centred(self):

        left_margin, right_margin = self.horizontal_margin
        return abs(left_margin - right_margin)/float(min(left_margin, right_margin)) < .1

    ##############################################

    @property
    def is_left_justified(self):

        # value indicates column

        page_width = self.text_page.interval.x.length()
        left_margin, right_margin = self.horizontal_margin
        return left_margin/float(page_width) # < .1

    ##############################################

    @property
    def y_rank(self):
        return self._y_rank

    ##############################################

    @y_rank.setter
    def y_rank(self, y_rank):
        self._y_rank = y_rank

    ##############################################

    @property
    def is_right_justified(self):

        page_width = self.text_page.interval.x.length()
        left_margin, right_margin = self.horizontal_margin
        return right_margin/float(page_width) # < .1

    ##############################################

    @property
    def y_inf(self):
        return self._interval.y.inf

    ##############################################
        
    @property
    def number_of_styles(self):

        return sum([line.number_of_styles for line in self._lines])

    ##############################################

    def __lt__(self, other):

        return self.y_inf < other.y_inf

    ##############################################

    def line_iterator(self):

        return iter(self._lines)

    ##############################################

    def append(self, line):

        self._lines.append(line)
        if self._text:
            self._text += ' '
        self._text += str(line)
        if self._interval is not None:
            self._interval |= line.interval
        else:
            self._interval = line.interval

    ##############################################
 
    @property
    def style_frequencies(self):

        """ Return an :obj:`TextStyleFrequencies` instance for the line. """

        if self._style_frequencies is None:
            self._style_frequencies = TextStyleFrequencies()
            for line in self.line_iterator():
                self._style_frequencies += line.style_frequencies()

        return self._style_frequencies

    ##############################################
 
    @property
    def main_style(self):

        """ Return the style having the largest occurence. """

        main_style_id = self.style_frequencies.max().style_id
        return self.styles[main_style_id]

####################################################################################################

class TextLine(TextBase):

    """ This class represents a line of text.

    A line is made of several spans where the number of
    spans is identical to the number of styles of the line.
    """

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
        self._text += str(span)

    ##############################################
        
    def style_frequencies(self):

        """ Return an :obj:`TextStyleFrequencies` instance for the line. """

        style_frequencies = TextStyleFrequencies()
        for span in self:
            style_id = span.style.id
            count = len(span)
            style_frequencies.fill(style_id, count)
        
        return style_frequencies

####################################################################################################

class TextSpan(TextBase):

    """ This class represents a span that is a piece of text having only one style.

    A TextSpan corresponds here to the subset of chars having the same style within a C span.
    """
    
    ##############################################

    def __init__(self, text, style):

        super(TextSpan, self).__init__(text)

        self.style = style

####################################################################################################
# 
# End
# 
####################################################################################################
