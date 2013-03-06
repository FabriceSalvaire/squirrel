####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

import numpy as np

####################################################################################################

from Babel.Tools.Math import rint
from Babel.Tools.Interval import IntervalInfOpen, IntervalSupOpen

####################################################################################################

def compute_binning(interval, number_of_bins=None, bin_size=None):

    """ Compute an histogram binning.

    Return the 3-tuple (interval, number_of_bins, bin_size).
    """

    if number_of_bins is None and bin_size is None:
        raise ValueError()

    interval = IntervalSupOpen(interval)
    if bin_size is not None:
        number_of_bins = rint(interval.length() / float(bin_size))
        interval.sup = interval.inf + number_of_bins * bin_size
    else:
        bin_size = interval.length() / number_of_bins

    return interval, number_of_bins, bin_size

####################################################################################################

class Histogram(object):

    ##############################################

    def __init__(self, interval, number_of_bins=None, bin_size=None):

        interval, number_of_bins, bin_size = compute_binning(interval, number_of_bins, bin_size)

        self._interval = interval
        self._number_of_bins = number_of_bins
        self._bin_size = bin_size
        self._bins = self._make_bins()
        self._bin_contents = self._make_bin_contents()

    ##############################################
        
    def _make_bins(self):

        bins = np.zeros(self._number_of_bins +2)
        bins[0] = bins[self._number_of_bins +1] = float('nan')
        bins[1:self._number_of_bins +1] = np.arange(start=self._interval.inf,
                                                    stop=self._interval.sup + self._bin_size,
                                                    step=self._bin_size)

        return bins

    ##############################################
        
    def _make_bin_contents(self):

        return np.zeros(self._number_of_bins +2)

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
    def bin_size(self):

        return self._bin_size

    ##############################################
        
    @property
    def bins(self):

        return self._bins

    ##############################################
        
    @property
    def bin_contents(self):

        return self._bin_contents

    ##############################################

    def bin_index_iterator(self):

        return xrange(1, self._number_of_bins +1)

    ##############################################

    def bin_and_overflow_index_iterator(self):

        return xrange(self._number_of_bins +2)

    ##############################################

    def __str__(self):

        string_format = """
Histogram:
  interval: %s
  number of bins: %u
  bin size: %g
"""

        message = string_format % (str(self._interval), self._number_of_bins, self._bin_size)
        for i in self.bin_and_overflow_index_iterator():
            if i:
                interval_class = IntervalInfOpen
            else:
                interval_class = IntervalSupOpen
            interval = interval_class(self._bins[i], self._bins[i+1])
            message += '  %s = %g\n' % (str(interval), self._bin_contents[i])
        
        return message

    ##############################################

    def find_bin(self, x):

        inf = self._interval.inf
        if x < inf:
            return 0
        elif x >= self._interval.sup:
            return self._number_of_bins +1
        else:
            return int((x - inf) / self._bin_size) +1

    ##############################################

    def fill(self, x, weight=1.):

        self._bin_contents[self.find_bin(x)] += weight

####################################################################################################
# 
# End
# 
####################################################################################################
