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

"""Defines language IDs.

Usage::

  int(LanguageId.en)
  LanguageId.en.name
  LanguageId(1)
  LanguageId['en']
"""

# Fixme: check api, en vs english

####################################################################################################

import enum

####################################################################################################

class LanguageId(enum.IntEnum):

    unknown = 0 # auto()
    en = 1
    fr = 2

####################################################################################################

_LanguageId_to_str = [
    'unknown',
    'english',
    'french',
]

def languages():
    return _LanguageId_to_str

def language_id_to_str(i):
    return _LanguageId_to_str[i]
