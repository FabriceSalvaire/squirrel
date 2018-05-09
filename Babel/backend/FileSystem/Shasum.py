####################################################################################################
#
# Babel - An Electronic Document Management System
# Copyright (C) 2017 Fabrice Salvaire
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

import hashlib

####################################################################################################

def run_shasum(filename, algorithm=1, binary=False, text=True, universal=False, portable=False):

    # Fixme: Linux only

    if algorithm not in (1, 224, 256, 384, 512, 512224, 512256):
        raise ValueError

    args = ['shasum', '--algorithm=' + str(algorithm)]
    if text:
        args.append('--text')
    elif binary:
        args.append('--binary')
    elif universal:
         # read in Universal Newlines mode produces same digest on Windows/Unix/Mac
        args.append('--universal')
    elif portable:
         # to be deprecated
        args.append('--portable')
    args.append(filename)
    output = subprocess.check_output(args).decode('utf-8')
    shasum = output[:output.find(' ')]

    return shasum

####################################################################################################

def shasum(path, algorithm=1):

    # This module implements a common interface to many different secure hash and message digest
    # algorithms. Included are the FIPS secure hash algorithms SHA1, SHA224, SHA256, SHA384, and
    # SHA512 (defined in FIPS 180-2)

    if algorithm not in (1, 224, 256, 384, 512):
        raise ValueError

    hasher = hashlib.new('sha' + str(algorithm))
    with open(str(path), 'rb') as f:
         hasher.update(f.read())
    return hasher.hexdigest()
