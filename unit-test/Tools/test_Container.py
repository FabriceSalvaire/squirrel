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

from Babel.Tools.Container import Ring

####################################################################################################

class TestRing(unittest.TestCase):

    ##############################################

    def test_delete(self):

        ring = Ring(list(range(3)), closed=True)

        self.assertEqual(ring.current_index, 0)
        self.assertEqual(ring.current_item, 0)

        next(ring)
        self.assertEqual(ring.current_index, 1)
        self.assertEqual(ring.current_item, 1)

        next(ring)
        self.assertEqual(ring.current_index, 2)
        self.assertEqual(ring.current_item, 2)

        next(ring)
        self.assertEqual(ring.current_index, 0)
        self.assertEqual(ring.current_item, 0)

        ring.previous()
        self.assertEqual(ring.current_index, 2)
        self.assertEqual(ring.current_item, 2)

        ring.previous()
        self.assertEqual(ring.current_index, 1)
        self.assertEqual(ring.current_item, 1)

        ring.previous()
        self.assertEqual(ring.current_index, 0)
        self.assertEqual(ring.current_item, 0)

        ring.delete(0)
        self.assertEqual(ring.current_index, 0)
        self.assertEqual(ring.current_item, 1)

        ring.delete(1)
        self.assertEqual(ring.current_index, 0)
        self.assertEqual(ring.current_item, 2)

        ring.delete(2)
        self.assertIsNone(ring.current_index)

        ring = Ring(list(range(3)), closed=True)

        ring.delete(2)
        self.assertEqual(ring.current_index, 0)
        self.assertEqual(ring.current_item, 0)

        next(ring)
        ring.delete(0)
        self.assertEqual(ring.current_index, 0)
        self.assertEqual(ring.current_item, 1)

        ring = Ring(list(range(3)), closed=True)

        next(ring)
        next(ring)
        ring.delete(2)
        self.assertEqual(ring.current_index, 0)
        self.assertEqual(ring.current_item, 0)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
