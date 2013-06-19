####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################
#
#                                              Audit
#
# - 17/06/2013 Fabrice
#   attribute -> _attribute
#
####################################################################################################

####################################################################################################

from Babel.Tools.DictionaryTools import DictInitialised

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
        rank=None, # font size rank, rank 0 for the largest
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

class TextStyles(dict):

    ##############################################

    def register_style(self, style):

        self[style.id] = style

    ##############################################

    def sort(self):

        """ Sort the styles by font size. """

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

class TextStyleFrequency(DictInitialised):

    __REQUIRED_ATTRIBUTES__ = (
        'style_id',
        'count',
        )

    ##############################################

    def __cmp__(self, other):

        return cmp(self.count, other.count)

    ##############################################

    def __iadd__(self, count):

        self.count += count

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
            self[style_id] = count # TextStyleFrequency(style_id, count) ?
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
# 
# End
# 
####################################################################################################
