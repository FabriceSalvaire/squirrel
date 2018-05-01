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

from ..Tags import TagsAbc

####################################################################################################

class Tags(TagsAbc):

    __language__ = 'fr'

    __tags__ = {
        'ADJ': 'Adjectif',                  #  0
        'ADJ:dem': 'Adjectif démonstratif', #  1
        'ADJ:int': 'Adjectif interrogatif', #  2
        'ADJ:ind': 'Adjectif indéfini',     #  3
        'ADJ:num': 'Adjectif numérique',    #  4
        'ADJ:pos': 'Adjectif possessif',    #  5
        'ADV': 'Adverbe',                   #  6
        'ART:def': 'Article défini',        #  7
        'ART:ind': 'Article indéfini',      #  8
        'AUX': 'Auxiliaire',                #  9
        'CON': 'Conjonction',               # 10
        'LIA': "Liaison euphonique (l')",   # 11
        'NOM': 'Nom commun',                # 12
        'ONO': 'Onomatopée',                # 13
        'PRE': 'Préposition',               # 14
        'PRO:dem': 'Pronom démonstratif',   # 15
        'PRO:ind': 'Pronom indéfini',       # 16
        'PRO:int': 'Pronom interrogatif',   # 17
        'PRO:per': 'Pronom personnel',      # 18
        'PRO:pos': 'Pronom possessif',      # 19
        'PRO:rel': 'Pronom relatif',        # 20
        'VER': 'Verbe',                     # 21
    }

    __noun_tags__ = ('NOM')
