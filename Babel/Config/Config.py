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

import os

from ..FileSystem.File import Directory

####################################################################################################

class Path:

    # Fixme: Linux

    CONFIG_DIRECTORY = Directory(os.path.join(os.environ['HOME'], '.config', 'babel'))

    # data_directory = Directory(os.path.join(os.environ['HOME'], '.local', 'share', 'data', 'babel'))
    DATA_DIRECTORY = Directory(os.path.join(os.environ['HOME'], '.local', 'babel'))

    ##############################################

    @classmethod
    def join_config_directory(cls, *args):
        return cls.CONFIG_DIRECTORY.join_path(*args)

    ##############################################

    @classmethod
    def join_data_directory(cls, *args):
        return cls.DATA_DIRECTORY.join_path(*args)

    ##############################################

    @classmethod
    def make_user_directory(cls):

        for directory in (
                cls.CONFIG_DIRECTORY,
                cls.DATA_DIRECTORY,
        ):
            directory = str(directory) # Fixme: api
            if not os.path.exists(directory):
                os.mkdir(directory)

####################################################################################################

class DataBase:

    @classmethod
    def document_database(cls):
        return Path.join_data_directory('document-database.sqlite')

    @classmethod
    def whoosh_database(cls):
        return Path.join_data_directory('whoosh-database')

####################################################################################################

class Help:

    host = 'localhost'
    url_scheme = 'http'
    url_path_pattern = '/'

####################################################################################################

class Shortcut:
    pass
