####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

import os

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QColor

####################################################################################################

class Path(object):

    config_directory = os.path.join(os.environ['HOME'], '.config', 'babel')

    # data_directory = os.path.join(os.environ['HOME'], '.local', 'share', 'data', 'babel')
    data_directory = os.path.join(os.environ['HOME'], '.local', 'babel')

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
