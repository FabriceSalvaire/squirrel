####################################################################################################
#
# Babel - An Electronic Document Management System
# Copyright (C) 2018 Fabrice Salvaire
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

"""Implement Part-of-Speech Tags.
"""

####################################################################################################

class Tag:

    ##############################################

    def __init__(self, tag_id, tag, is_noun=False):

        self._id = tag_id
        self._tag = tag
        self._is_noun = is_noun

    ##############################################

    def __str__(self):
        return self._tag

    ##############################################

    def __int__(self):
        return self._id

    ##############################################

    def __repr__(self):
        return self._tag

    ##############################################

    def __lt__(self, other):
        return self._id < other._id

    ##############################################

    @property
    def is_noun(self):
        return self._is_noun

####################################################################################################

class TagsMetaclass(type):

    __languages__ = {}

    ##############################################

    def __init__(cls, name, bases, namespace):

        type.__init__(cls, name, bases, namespace)

        language = cls.__language__
        if language:
            TagsMetaclass.__languages__[language] = cls()

####################################################################################################

class TagRegistry:
    def __getitem__(self, language):
        return TagsMetaclass.__languages__[language]

####################################################################################################

class TagsAbc(metaclass=TagsMetaclass):

    __language__ = None

    __tags__ = {
        # 'tag': definition
    }

    __noun_tags__ = ()

    ##############################################

    def __init__(self):

        self._tag_map = {tag:Tag(i, tag, tag in self.__noun_tags__)
                         for i, tag in
                         enumerate(self.__tags__.keys())}
        self._tag_map.update({int(tag):tag for tag in self._tag_map.values()})
        # 64-bit integer : 1 << 63 is sign bit
        # we encode up to 63 tags with a single integer
        self._require_extended_tag = len(self) > 63

    ##############################################

    @property
    def language(self):
        return self.__language__

    @property
    def require_extended_tag(self):
        return self._require_extended_tag

    ##############################################

    def __len__(self):
        return len(self.__tags__)

    ##############################################

    def __contains__(self, name):
        return name in self.__tags__

    ##############################################

    def __getitem__(self, key):
        return self._tag_map[key]

    ##############################################

    def encode_tags(self, tags):

        bits = 0
        for tag in tags:
            if not isinstance(tag, Tag):
                tag = self[tag]
            bits += 1 << int(tag)

        if self._require_extended_tag:
            return bits & ((1 << 63) -1), bits >> 63
        else:
            return bits

    ##############################################

    def _decode_tags(self, bits, offset=0):

        return [self[i + offset] for i in range(63) if bits & (1 << i)]

    ##############################################

    def decode_tags(self, *bits):

        tags = self._decode_tags(bits[0])
        if self._require_extended_tag:
            tags += self._decode_tags(bits[1], 63)
        return tags
