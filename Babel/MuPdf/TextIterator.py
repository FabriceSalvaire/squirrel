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

import Babel.MuPdf as _mupdf

####################################################################################################

class GenericIterator(object):

    _getter = None

    ##############################################

    def __init__(self, obj):

        self._obj = obj
        self._index = 0
        self._size = self._obj.len

    ##############################################

    def __iter__(self):

        return self

    ##############################################

    def __next__(self):

        if self._index < self._size:
            item = self._getter(self._obj, self._index)
            self._index += 1
            return item
        else:
            raise StopIteration

    # Py2
    next = __next__

####################################################################################################

# class TextBlockIterator(GenericIterator):
#     _getter = _mupdf.get_text_block

# class TextLineIterator(GenericIterator):
#     _getter = _mupdf.get_text_line

# class TextCharIterator(GenericIterator):
#     _getter = _mupdf.get_text_char

####################################################################################################

class TextSpanIterator(object):

    ##############################################

    def __init__(self, text_line):

        self._text_line = text_line
        self._span = self._text_line.first_span

    ##############################################

    def __iter__(self):

        return self

    ##############################################

    def __next__(self):

        if self._span:
            span = self._span
            self._span = span.next
            return span
        else:
            raise StopIteration

    # Py2
    next = __next__

####################################################################################################
#
# End
#
####################################################################################################
