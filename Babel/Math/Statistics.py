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

import math

####################################################################################################

class Gaussian:

    ##############################################

    def __init__(self, mean, sigma):

        self._mean = mean
        self._sigma = sigma
        self._inverse_sigma = 1. / self.sigma

    ##############################################

    @property
    def mean(self):
        return self._mean

    @property
    def sigma(self):
        return self._sigma

    ##############################################

    def __call__(self, x):

        return math.exp(-((self._mean - x)*self._inverse_sigma)**2)
