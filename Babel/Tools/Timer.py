####################################################################################################
#
# Babel - A Bibliography Manager
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

import logging
import time

from GVLab.C.PlatformC import calibrate_cpu_clock, CpuTSC

####################################################################################################

class TimeTracker(object):

    __cpu_clock_frequency__ = calibrate_cpu_clock(1)

    ##############################################

    def __init__(self, recalibrate=False, waiting_time=1):

        if recalibrate:
            self._cpu_clock_frequency = calibrate_cpu_clock(waiting_time)
        else:
            self._cpu_clock_frequency = TimeTracker.__cpu_clock_frequency__
        self._activities = {}

    ##############################################

    def __contains__(self, name):

        return name in self._activities

    ##############################################

    def __getitem__(self, name):

        return self._activities[name]

    ##############################################

    def __iter__(self):

        return self._activities.itervalues()

    ##############################################

    @property
    def cpu_clock_frequency(self):
        return self._cpu_clock_frequency

    ##############################################

    def add_activity(self, name):

        if name not in self: 
            activity = TimeTrackerActivity(self, name)
            self._activities[name] = activity
            return activity
        else:
            raise NameError("Activity %s alaready exists" % (name))

    ##############################################

    def ensure_activity(self, name):

        if name not in self: 
            return self.add_activity(name)
        else:
            return self[name]

####################################################################################################

class TimeTrackerActivity(object):

    ##############################################

    def __init__(self, time_tracker, name):

        self._time_tracker = time_tracker
        self._name = name

        self._cpu_tsc = CpuTSC(self._time_tracker.cpu_clock_frequency)
        self._number_of_cycles = 0L

    ##############################################

    @property
    def name(self):
        return self._name

    ##############################################

    @property
    def number_of_cycles(self):
        return self._number_of_cycles

    ##############################################

    @property
    def time(self):
        return self._number_of_cycles / float(self._time_tracker.cpu_clock_frequency)

    ##############################################

    def start(self):

        self._cpu_tsc.set()

    ##############################################

    def stop(self):

        self._number_of_cycles += self._cpu_tsc.delta(True)

####################################################################################################

class Timer(object):

    _logger = logging.getLogger(__name__ + '.Timer')

    ##############################################

    def __init__(self):

        self.start(verbose=False)

    ##############################################

    def start(self, verbose=True):
        if verbose:
            self._logger.info('Start timer')
        self.t0 = time.time()
        self.t1 = 0

    ##############################################

    def stop(self, verbose=True):
        self.t1 = time.time()
        if verbose:
            self._logger.info('Stop timer')

    ##############################################

    def delta_time(self):
        
        if self.t1 == 0:
            self.stop()

        dt = self.t1 - self.t0 # s
        s = int(dt)
        ms = int((dt * 1e3) % 1e3)       
        us = int((dt * 1e6) % 1e3)
        
        return (s, ms, us)

    ##############################################

    def __str__(self):

        return '%u s %u ms %u us' % self.delta_time()

    ##############################################

    def delta_time_string(self):

        return 'Delta time: %u s %u ms %u us' % self.delta_time()

####################################################################################################
#
# End
#
####################################################################################################
