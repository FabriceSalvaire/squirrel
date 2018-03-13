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

import os
from pathlib import Path

####################################################################################################

def to_absolute_path(path):

    # Expand ~ . and Remove trailing '/'

    # return os.path.abspath(os.path.expanduser(path))
    return Path(path).expanduser().resolve()

####################################################################################################

def find(file_name, directories):

    if isinstance(directories, (str, Path)):
        directories = (directories,)

    for directory in directories:
        for directory_path, _, file_names in os.walk(str(directory)):
            if file_name in file_names:
                return Path(directory_path).joinpath(file_name)

    raise NameError("File {} not found in directories {}".format(file_name, directories))
