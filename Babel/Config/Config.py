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

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

####################################################################################################

class Path(object):

    config_directory = os.path.join(os.environ['HOME'], '.config', 'babel')

    # data_directory = os.path.join(os.environ['HOME'], '.local', 'share', 'data', 'babel')
    data_directory = os.path.join(os.environ['HOME'], '.local', 'babel')

####################################################################################################

class DataBase(object):

    file_database = os.path.join(Path.data_directory, 'file-database.sqlite')
    word_database = os.path.join(Path.data_directory, 'word-database.sqlite')
    word_document_database = os.path.join(Path.data_directory, 'word-document-database.sqlite')

####################################################################################################

class Email(object):

    from_address = 'fabrice.salvaire@orange.fr'
    to_address = ['fabrice.salvaire@orange.fr',]

####################################################################################################

class Help(object):

    host = 'localhost'
    url_scheme = 'http'
    url_path_pattern = '/'

####################################################################################################

class RedmineRest(object):

    url = 'http://loalhost/redmine/'
    key = '02caaf292242bbfde9000291cb9955337fa87518'
    project = 'Babel'

####################################################################################################

class Shortcut(object):

    pass

####################################################################################################
#
# End
#
####################################################################################################
