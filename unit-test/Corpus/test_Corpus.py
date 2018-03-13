####################################################################################################
#
# Babel - An Electronic Document Management System
# Copyright (C) 2017 Fabrice Salvaire
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

import unittest

from Babel.Corpus import tag_registry

####################################################################################################

class TestTags(unittest.TestCase):

    ##############################################

    def test(self):

        en_tags = tag_registry['en']
        # print(en_tags._tag_map)

        for tags in (
                (0, 61),
                (0, 62),
                (0, 63),
                (0, 64),
                (0, 65),
                (0, len(en_tags) -1),
                (0, 61, 62, 63, 64, 65, len(en_tags) -1),
                ):
            tags = [en_tags[i] for i in tags]
            bits = en_tags.encode_tags(tags)
            self.assertEqual(tags, en_tags.decode_tags(*bits))

####################################################################################################

if __name__ == '__main__':

    unittest.main()
