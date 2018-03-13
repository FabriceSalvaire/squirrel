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

from Babel.Math.Interval import *

####################################################################################################

class TestInterval(unittest.TestCase):

    ##############################################

    def test(self):

        ###########################################
        #
        # Test argument validity

        with self.assertRaises(ValueError):
            Interval(1, 0)

        ###########################################
        #
        # Test __getitem__ interface

        i1 = Interval(1, 10)
        for i in (i1,
                  (1, 10),
                  [1, 10],
                  ):
            self.assertEqual(i1, Interval(i))

        ###########################################
        #
        # Test copy

        self.assertEqual(i1, i1.copy())

        ###########################################
        #
        # Test length

        self.assertEqual(i1.length(), 9)

        i1 = IntervalInt(1.1, 10.1)
        self.assertEqual(i1.length(), 10)

        ###########################################
        #
        # Test empty

        empty = Interval(None, None)
        self.assertTrue(empty.is_empty())

        ###########################################
        #
        # Test union

        # Indenp
        i1 = Interval(1, 10)
        self.assertEqual(i1 | i1, i1)

        # Inside
        i1 = Interval(1, 20)
        i2 = Interval(5, 15)
        self.assertEqual(i1 | i2, i1)
        self.assertEqual(i2 | i1, i1)

        # Overlap
        i1 = Interval(1, 10)
        i2 = Interval(5, 15)
        i1_i2_union = Interval(1, 15)
        self.assertEqual(i1 | i2, i1_i2_union)
        self.assertEqual(i2 | i1, i1_i2_union)

        # Inf = Sup
        i1 = Interval(1, 10)
        i2 = Interval(10, 15)
        self.assertEqual(i1 | i2, i1_i2_union)
        self.assertEqual(i2 | i1, i1_i2_union)

        # Outside
        i1 = Interval(1, 10)
        i2 = Interval(11, 15)
        self.assertEqual(i1 | i2, i1_i2_union)
        self.assertEqual(i2 | i1, i1_i2_union)

        # |=
        i1 = Interval(0, 10)
        i2 = Interval(5, 15)
        i1 |= i2
        self.assertEqual(i1, Interval(0, 15))

        ###########################################
        #
        # Test intersection

        # Indenp
        i1 = Interval(1, 10)
        self.assertEqual(i1 & i1, i1)

        # Inside
        i1 = Interval(1, 20)
        i2 = Interval(5, 15)
        self.assertEqual(i1 & i2, i2)
        self.assertEqual(i2 & i1, i2)

        # Overlap
        i1 = Interval(1, 10)
        i2 = Interval(5, 15)
        i1_i2_intersection = Interval(5, 10)
        self.assertEqual(i1 & i2, i1_i2_intersection)
        self.assertEqual(i2 & i1, i1_i2_intersection)

        # Inf = Sup
        i1 = Interval(1, 10)
        i2 = Interval(10, 15)
        i1_i2_intersection = Interval(10, 10)
        self.assertEqual(i1 & i2, i1_i2_intersection)
        self.assertEqual(i2 & i1, i1_i2_intersection)

        # Outside
        i1 = Interval(1, 10)
        i2 = Interval(11, 15)
        self.assertEqual(i1 & i2, empty)
        self.assertEqual(i2 & i1, empty)

        # &=
        i1 = Interval(0, 10)
        i2 = Interval(5, 15)
        i1 &= i2
        self.assertEqual(i1, Interval(5, 10))

        ###########################################
        #
        # Test init with Interval isntance

        i1 = Interval(0, 10)
        self.assertEqual(i1, Interval(i1))
        self.assertEqual(i1, IntervalInt(i1))

####################################################################################################

class TestInterval2D(unittest.TestCase):

    ##############################################

    def test(self):

        ###########################################
        #
        # Test __getitem__ interface

        i1 = Interval2D((1, 10), (10, 100))

        for x, y in ((Interval(1, 10), Interval(10, 100)),
                     ([1, 10], [10, 100]),
                     ):
            self.assertEqual(i1, Interval2D(x, y))

        ###########################################
        #
        # Test copy

        self.assertEqual(i1, i1.copy())

        ###########################################
        #
        # Test union

        i1 = Interval2D((1, 10), (10, 100))
        i2 = Interval2D((5, 15), (50, 150))

        i1_i2_union = Interval2D((1, 15), (10, 150))
        self.assertEqual(i1 | i2, i1_i2_union)

        i1 |= i2
        self.assertEqual(i1, i1_i2_union)

        ###########################################
        #
        # Test intersection

        i1 = Interval2D((1, 10), (10, 100))
        i2 = Interval2D((5, 15), (50, 150))

        i1_i2_intersection = Interval2D((5, 10), (50, 100))
        self.assertEqual(i1 & i2, i1_i2_intersection)

        i1 &= i2
        self.assertEqual(i1, i1_i2_intersection)

        ###########################################
        #
        # Test size

        i1 = Interval2D((1, 10), (10, 100))

        self.assertEqual(i1.size(), (9, 90))

        i1 = IntervalInt2D((1.1, 10.1), (10.1, 100.1))
        self.assertEqual(i1.size(), (10, 91))

####################################################################################################

class TestIntervalSupOpen(unittest.TestCase):

    ##############################################

    def test(self):

        ###########################################
        #
        # Test intersection

        empty = IntervalSupOpen(None, None)

        # Indenp
        i1 = IntervalSupOpen(1, 10)
        self.assertEqual(i1 & i1, i1)

        # Inside
        i1 = IntervalSupOpen(1, 20)
        i2 = IntervalSupOpen(5, 15)
        self.assertEqual(i1 & i2, i2)
        self.assertEqual(i2 & i1, i2)

        # Overlap
        i1 = IntervalSupOpen(1, 10)
        i2 = IntervalSupOpen(5, 15)
        i1_i2_intersection = IntervalSupOpen(5, 10)
        self.assertEqual(i1 & i2, i1_i2_intersection)
        self.assertEqual(i2 & i1, i1_i2_intersection)

        # Inf = Sup
        i1 = IntervalSupOpen(1, 10)
        i2 = IntervalSupOpen(10, 15)
        i1_i2_intersection = IntervalSupOpen(10, 10)
        self.assertEqual(i1 & i2, empty)
        self.assertEqual(i2 & i1, empty)

        # Outside
        i1 = IntervalSupOpen(1, 10)
        i2 = IntervalSupOpen(11, 15)
        self.assertEqual(i1 & i2, empty)
        self.assertEqual(i2 & i1, empty)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
