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

__all__ = [
    'Binning1D',
]

####################################################################################################

import numpy as np

from Babel.Math.Interval import Interval, MinusInfinity, PlusInfinity
from Babel.Math.Functions import rint

####################################################################################################

class Binning1D:

    _under_flow_bin = 0
    _first_bin = 1

    ##############################################

    def __init__(self, interval, bin_width=None, number_of_bins=None,):

        if bin_width is None and number_of_bins is None:
            raise ValueError("...")

        self._interval = Interval(interval, right_open=True)
        if bin_width is not None:
            # Method to adjust the x range:
            #  - round sup, inf or both
            #  - extend sup, inf or both
            self._bin_width = float(bin_width)
            self._number_of_bins = rint(self._interval.length() / self._bin_width)
            self._interval.sup = self._interval.inf + self._number_of_bins * self._bin_width
        else:
            self._number_of_bins = int(number_of_bins)
            self._bin_width = self._interval.length() / self._number_of_bins

        self._last_bin = self._number_of_bins
        self._over_flow_bin = self._number_of_bins +1
        self._array_size = self._over_flow_bin +1

        self._inverse_bin_width = 1./self._bin_width

    ##############################################

    @property
    def interval(self):

        return self._interval

    ##############################################

    @property
    def number_of_bins(self):

        return self._number_of_bins

    ##############################################

    @property
    def under_flow_bin(self):

        return self._under_flow_bin

    ##############################################

    @property
    def first_bin(self):

        return self._first_bin

    ##############################################

    @property
    def last_bin(self):

        return self._over_flow_bin -1

    ##############################################

    @property
    def over_flow_bin(self):

        return self._over_flow_bin

    ##############################################

    @property
    def array_size(self):

        return self._array_size

    ##############################################

    @property
    def bin_width(self):

        return self._bin_width

    ##############################################

    def __eq__(self, other):

        return (self._interval == other._interval
                and self._number_of_bins == other._number_of_bins)

   ###############################################

    def _check_bin_index(self, i, xflow=False):

        if xflow:
            if self._over_flow_bin < i < self._under_flow_bin:
                raise IndexError
        else:
            if self._over_flow_bin <= i <= self._under_flow_bin:
                raise IndexError

    ##############################################

    def clone(self):

        return self.__class__(self._interval, number_of_bins=self._number_of_bins)

    ##############################################

    def bin_interval(self, i):

        if i == self._under_flow_bin:
            return Interval(MinusInfinity, self._interval.inf, left_open=True, right_open=True)
        elif i == self._over_flow_bin:
            return Interval(self._interval.sup, PlusInfinity, right_open=True)
        else:
            return Interval(self.bin_lower_edge(i), self.bin_upper_edge(i), right_open=True)

   ###############################################

    def _bin_edge(self, i, offset=0):

        self._check_bin_index(i, xflow=False)
        return self._interval.inf + (i - 1 + offset)*self._bin_width

   ###############################################

    def bin_lower_edge(self, i):

        return self._bin_edge(i)

   ###############################################

    def bin_upper_edge(self, i):

        return self._bin_edge(i, offset=1)

   ###############################################

    def bin_center(self, i):

        return self._bin_edge(i, offset=.5)

    ##############################################

    def bins(self):

        bins = np.zeros(self._number_of_bins +2)
        bins[self._under_flow_bin] = MinusInfinity
        bins[self._over_flow_bin] = PlusInfinity
        bins[self._first_bin:self._under_flow_bin] = \
            np.arange(start=self._interval.inf,
                      stop=self._interval.sup + self._bin_width,
                      step=self._bin_width)

        return bins

    ##############################################

    def bin_centers(self):

        return np.linspace(self.bin_center(self._first_bin),
                           self.bin_center(self._last_bin),
                           self._number_of_bins)

    ##############################################

    def bin_slice(self, xflow=False):

        if xflow:
            return slice(self._under_flow_bin, self._array_size)
        else:
            return slice(self._first_bin, self._over_flow_bin)

    ##############################################

    def bin_iterator(self, xflow=False):

        if xflow:
            return range(self._under_flow_bin, self._array_size)
        else:
            return range(self._first_bin, self._over_flow_bin)

   ###############################################

    def find_bin(self, x):

        inf = self._interval.inf
        if x < inf:
            return self._under_flow_bin
        elif x >= self._interval.sup:
            return self._over_flow_bin
        else:
            return int(self._inverse_bin_width * (x - inf)) +1

   ###############################################

    def __str__(self):

        string_format = """
Binning 1D
  interval: %s
  number of bins: %u
  bin width: %g
"""

        text = string_format % (str(self._interval), self._number_of_bins, self._bin_width)
        for i in self.bin_iterator(xflow=True):
            # Fixme: 3u count number of digits
            text += '  %3u ' % i + str(self.bin_interval(i)) + '\n'

        return text

   ###############################################

    def sub_interval(self, bin_range):

        inf = max(self.first_bin, bin_range.inf)
        sup = min(self.last_bin, bin_range.sup)

        return Interval(self.bin_lower_edge(inf),
                        self.bin_upper_edge(sup))

   ###############################################

    def sub_binning(self, interval):

        return self.__class__(interval, self._bin_width)
