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

####################################################################################################

def create_user_directories(path_config):

    for purpose, directory in (
        ('config', path_config.config_directory),
        ('data', path_config.data_directory),
        ):
        create_user_directory(purpose, directory)

####################################################################################################

def create_user_directory(purpose, directory):

    if not os.path.isabs(directory):
        raise ValueError("%s directory must be absolut (given is %s)" %
                         (purpose.title(), directory))
    if not os.path.exists(directory):
        os.mkdir(directory)
    elif not os.path.isdir(directory):
        raise ValueError("Path for %s directory is not a directory (given is %s)" %
                         (purpose, directory))
