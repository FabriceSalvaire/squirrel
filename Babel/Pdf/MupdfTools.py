####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################
# 
#                                              audit 
# 
# - 07/08/2013 Fabrice
#   xx
# 
####################################################################################################

####################################################################################################

import mupdf as cmupdf
from MuPDF import *

####################################################################################################

from .TextStyle import TextStyle
from Babel.Tools.Interval import IntervalInt2D

####################################################################################################

def indent_line(text, indent_level, indent_pattern='  '):

    # Fixme: not here, purpose

    return indent_pattern*indent_level + text + '\n'

####################################################################################################

def get_font_name(font):

    """ Return the name of a MuPDF font. """

    font_name = cmupdf.get_font_name(font)
    i = font_name.find('+')
    if i:
        font_name = font_name[i+1:] 

    return font_name

####################################################################################################

def format_bounding_box(obj):

    return "[%g %g %g %g]" % (obj.bbox.x0, obj.bbox.y0,
                              obj.bbox.x1, obj.bbox.y1)

####################################################################################################

def to_interval(bounding_box):

    """ Convert a MuPDF bounding box to an :obj:`Babel.Tools.Interval.IntervalInt2D` object. """

    return IntervalInt2D((bounding_box.x0, bounding_box.x1),
                         (bounding_box.y0, bounding_box.y1))

####################################################################################################

def span_to_string(span):

    """ Return the unicode string corresponding to a MuPDF span. """

    span_text = u''
    for char in TextCharIterator(span):
        span_text += unichr(char.c)
    span_text = span_text.rstrip()
    
    return span_text

####################################################################################################
    
def to_text_style(style):

    """ Convert a MuPDF style instance to a :obj:`.TextStyle` object. """

    font = style.font
    text_style = TextStyle(id=style.id,
                           font_family=get_font_name(font),
                           font_size=style.size,
                           is_bold=bool(cmupdf.font_is_bold(font)),
                           is_italic=bool(cmupdf.font_is_italic(font)),
                           )
    
    return text_style

####################################################################################################
# 
# End
# 
####################################################################################################