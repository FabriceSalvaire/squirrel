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
#
#                                              Audit
#
# - 00/00/2010 Fabrice
#   xx
#
####################################################################################################

####################################################################################################

import os
import subprocess

####################################################################################################

# From proc(5)
_proc_stat_fields = [
    'pid', # %d The process ID.
    'comm', # %s The filename of the executable, in parentheses.  This is visible whether or not the
            # executable is swapped out.
    'state', # %c One character from the string "RSDZTW" where R is running, S is sleeping in an
             # interruptible wait, D is waiting in uninterruptible disk sleep, Z is zombie, T is
             # traced or stopped (on a signal), and W is paging.
    'ppid', # %d The PID of the parent.
    'pgrp', # %d The process group ID of the process.
    'session', # %d The session ID of the process.
    'tty_nr', # %d The tty the process uses.
    'tpgid', # %d The process group ID of the process which currently owns the tty that the process
             # is connected to.
    'flags', # %lu The kernel flags word of the process. For bit meanings, see the PF_* defines in
             # <linux/sched.h>.  Details depend on the kernel version.
    'minflt', # %lu The number of minor faults the process has made which have not required loading
              # a memory page from disk.
    'cminflt', # %lu The number of minor faults that the process's waited-for children have made.
    'majflt', # %lu The number of major faults the process has made which have required loading a
              # memory page from disk.
    'cmajflt', # %lu The number of major faults that the process's waited-for children have made.
    'utime', # %lu The number of jiffies that this process has been scheduled in user mode.
    'stime', # %lu The number of jiffies that this process has been scheduled in kernel mode.
    'cutime', # %ld The number of jiffies that this process's waited-for children have been
              # scheduled in user mode. (See also times(2).)
    'cstime', # %ld The number of jiffies that this process's waited-for children have been
              # scheduled in kernel mode.
    'priority', # %ld The standard nice value, plus fifteen.  The value is never negative in the
                # kernel.
    'nice', # %ld The nice value ranges from 19 (nicest) to -19 (not nice to others).
    'num_threads', # %ld Number of threads in this process (since Linux 2.6).  Before kernel 2.6,
                   # this field was hard coded to 0 as a placeholder for an earlier removed field.
    'itrealvalue', # %ld The time in jiffies before the next SIGALRM is sent to the process due to
                   # an interval timer.  Since Kernel 2.6.17, this field is hard coded to 0.
    'starttime', # %lu The time in jiffies the process started after system boot.
    'vsize', # %lu Virtual memory size in bytes.
    'rss', # %ld Resident Set Size: number of pages the process has in real memory, minus 3 for
           # administrative purposes. This is just the pages which count towards text, data, or
           # stack space.  This does not include pages which have not been demand-loaded in, or
           # which are swapped out.
    'rlim', # %lu Current limit in bytes on the rss of the process (usually 4294967295 on i386).
    'startcode', # %lu The address above which program text can run.
    'endcode', # %lu The address below which program text can run.
    'startstack', # %lu The address of the start of the stack.
    'kstkesp', # %lu The current value of esp (stack pointer), as found in the kernel stack page for
               # the process.
    'kstkeip', # %lu The current EIP (instruction pointer).
    'signal', # %lu The bitmap of pending signals.
    'blocked', # %lu The bitmap of blocked signals.
    'sigignore', # %lu The bitmap of ignored signals.
    'sigcatch', # %lu The bitmap of caught signals.
    'wchan', # %lu This is the "channel" in which the process is waiting.  It is the address of a
             # system call, and can be looked up in a namelist if you need a textual name.  (If you
             # have an up-to-date /etc/psdatabase, then try ps -l to see the WCHAN field in action.)
    'nswap', # %lu Number of pages swapped (not maintained).
    'cnswap', # %lu Cumulative nswap for child processes (not maintained).
    'exit_signal', # %d Signal to be sent to parent when we die.
    'processor', # %d CPU number last executed on.
    'rt_priority', # %lu (since kernel 2.5.19) Real-time scheduling priority (see
                   # sched_setscheduler(2)).
    'policy', # %lu (since kernel 2.5.19) Scheduling policy (see sched_setscheduler(2)).
    'delayacct_blkio_ticks', # %llu (since Linux 2.6.18) Aggregated block I/O delays, measured in clock ticks (centiseconds).
]

_proc_statm_fields = [
    'size', # total program size
    'resident', # resident set size
    'share', # shared pages (from shared mappings)
    'text', # text (code)
    'lib', # library (unused in Linux 2.6)
    'data', # data + stack
    'dt', # dirty pages (unused in Linux 2.6)
    ]

_proc_files = (('stat', _proc_stat_fields),
               ('statm', _proc_statm_fields),
               )

_proc_fields = []
for filename, fields in _proc_files:
    for field in fields:
        _proc_fields.append(filename + '_' + field)

####################################################################################################

class ProcessInfo:

    ##############################################

    def __init__(self):

        object.__setattr__(self, 'pid', os.getpid())
        object.__setattr__(self, 'page_size', self._get_page_size())
        self.refresh()

    ##############################################

    def _get_page_size(self):

        process = subprocess.Popen(['/usr/bin/getconf', 'PAGESIZE'], stdout=subprocess.PIPE)
        process.wait()

        return int(process.stdout.readline().rstrip())

    ##############################################

    def __setattr__(self, name, value):

        raise NotImplementedError

    ##############################################

    def refresh(self):

        field_counter = 0
        for filename, fields in _proc_files:
            with open('/proc/%u/%s' % (self.pid, filename), 'r') as f:
              for value in f.read().rstrip().split(' ')[:len(fields)]:
                  if value.isdigit():
                      value = int(value)
                  field = _proc_fields[field_counter]
                  object.__setattr__(self, field, value)
                  field_counter += 1

    ##############################################

    @property
    def resident_memory_size_mb(self):

        """ Resident memory size in MB """

        return self.statm_resident * self.page_size / 1024**2
