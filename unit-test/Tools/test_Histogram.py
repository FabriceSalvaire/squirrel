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

from Babel.Math.Binning import Binning1D
from Babel.Math.Histogram import *

####################################################################################################

class TestHistogram(unittest.TestCase):

    ##############################################

    def test(self):

        Binning = Binning1D((0, 10), bin_width=1)
        histogram = Histogram(Binning)
        histogram.fill(1.5, weight=10)
        print(histogram)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
