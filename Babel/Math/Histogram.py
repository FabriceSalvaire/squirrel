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

import numpy as np

from Babel.Math.Binning import Binning1D
from Babel.Math.Interval import Interval

####################################################################################################

class Histogram:

    ##############################################

    def __init__(self, binning):

        # Fixme: direct mode

        if isinstance(binning, Binning1D):
            self._binning = binning
        else:
            raise ValueError

        array_size = self._binning.array_size
        self._accumulator = np.zeros(array_size)
        self._sum_weight_square = np.zeros(array_size)
        self._errors = np.zeros(array_size)

        self._errors_are_dirty = True

    ##############################################

    @property
    def binning(self):

        return self._binning

    ##############################################

    @property
    def accumulator(self):

        return self._accumulator

    ##############################################

    def __iadd__(self, obj):

        if self.is_consistent_with(obj):
            self._accumulator += obj._accumulator
        else:
            raise ValueError

    ##############################################

    def is_consistent_with(self, obj):

        return self._binning == obj._binning

    ##############################################

    def clear(self, value=.0):

        self._accumulator[:] = value
        self._sum_weight_square[:] = value**2
        self._errors_are_dirty = True

    ##############################################

    def fill(self, x, weight=1.):

        if weight < 0:
            raise ValueError

        i = self._binning.find_bin(x)
        self._accumulator[i] += weight
        # if weight == 1.: weight_square = 1.
        self._sum_weight_square[i] += weight**2
        self._errors_are_dirty = True

    ##############################################

    def compute_errors(self):

        if self._errors_are_dirty:
            self._errors = np.sqrt(self._sum_weight_square)

    ##############################################

    def get_bin_error(self, i):

        self.compute_errors()

        return self._errors[i]

    ##############################################

    def integral(self, interval=None, interval_x=None):

        if interval is None and interval_x is None:
            return self._accumulator.sum()
        else:
            if interval_x is not None:
                start = self.binning.find_bin(interval_x.inf)
                stop = self.binning.find_bin(interval_x.sup)
            else:
                start = interval.inf
                stop = interval.sup
            return self._accumulator[start:stop +1].sum(), Interval(start, stop)

    ##############################################

    def normalise(self, scale=1):

        self._accumulator /= self.integral()
        self._errors_are_dirty = True
        if scale != 1:
            self._accumulator *= scale

    ##############################################

    def to_graph(self):

        self.compute_errors()

        binning = self._binning
        bin_slice = binning.bin_slice()

        x_values = binning.bin_centers()

        y_values = np.copy(self._accumulator[bin_slice])
        y_errors = np.copy(self._errors[bin_slice])

        x_errors = np.empty(x_values.shape)
        x_errors[:] = .5*binning.bin_width

        return x_values, y_values, x_errors, y_errors

   ###############################################

    def __str__(self):

        binning = self._binning

        string_format = """
Histogram 1D
  interval: %s
  number of bins: %u
  bin width: %g
"""

        text = string_format % (str(binning._interval), binning._number_of_bins, binning._bin_width)
        for i in binning.bin_iterator(xflow=True):
            text += '%3u %s = %g +- %g\n' % (i,
                                             str(binning.bin_interval(i)),
                                             self._accumulator[i],
                                             self.get_bin_error(i),
                                             )

        return text

   ###############################################

    def find_non_zero_bin_range(self):

        inf = 0
        while self._accumulator[inf] == 0:
            inf += 1

        sup = len(self._accumulator) -1
        while self._accumulator[sup] == 0:
            sup -= 1

        return Interval(inf, sup)

   ###############################################

    def non_zero_bin_range_histogram(self):

        bin_range = self.find_non_zero_bin_range()
        print(bin_range)
        binning = self._binning.sub_binning(self._binning.sub_interval(bin_range))
        print(binning)
        histogram = self.__class__(binning)
        src_slice = slice(bin_range.inf, bin_range.sup +1)
        dst_slice = slice(binning.first_bin, binning.over_flow_bin)
        histogram._accumulator[dst_slice] = self._accumulator[src_slice]
        histogram._sum_weight_square[dst_slice] = self._sum_weight_square[src_slice]
        histogram._errors[dst_slice] = self._errors[src_slice]
        histogram.errors_are_dirty = False

        return histogram
