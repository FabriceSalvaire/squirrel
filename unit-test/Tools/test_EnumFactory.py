####################################################################################################
#
# Babel - An Electronic Document Management System
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

import unittest

####################################################################################################

from Babel.Tools.EnumFactory import *

####################################################################################################

class TestEnumFactory(unittest.TestCase):

    def test(self):

        enum1 = EnumFactory('Enum1', ('cst1', 'cst2'))

        self.assertEqual(enum1.cst1, 0)
        self.assertEqual(enum1.cst2, 1)
        self.assertEqual(len(enum1), 2)

        enum2 = ExplicitEnumFactory('Enum2', {'cst1':1, 'cst2':3})

        self.assertEqual(enum2.cst1, 1)
        self.assertEqual(enum2.cst2, 3)

        self.assertTrue(enum2.cst2 in enum2)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
