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

def XByte(x, power):
    return x * 1024**power

def to_XByte(x, power):
    return float(x)/1024**power

def KByte(x):
    return XByte(x, 1)

def to_KByte(x):
    return to_XByte(x, 1)

def MByte(x):
    return XByte(x, 2)

def to_MByte(x):
    return to_XByte(x, 2)

def GByte(x):
    return XByte(x, 3)

def to_GByte(x):
    return to_XByte(x, 3)

def TByte(x):
    return XByte(x, 4)

def to_TByte(x):
    return to_XByte(x, 4)
