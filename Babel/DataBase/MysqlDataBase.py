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

import logging

from Babel.Tools.Singleton import SingletonMetaClass
from .DataBase import DataBase

####################################################################################################

class MysqlDataBase(DataBase, metaclass=SingletonMetaClass):

    _logger = logging.getLogger(__name__)

    CONNECTION_STR = "mysql+oursql://{user_name}:{password}@{hostname}/{database}"

    ###############################################

    def __init__(self, database_config, echo=None):

        self._logger.debug("Open MySql Database %s", self.CONNECTION_STR)

        # Fixme: _ only used for one
        connection_keys =  {'hostname':database_config.hostname,
                            'database':database_config.database,
                            'user_name':database_config.user_name,
                            'password':database_config.password,
                            }
        connection_str = self.CONNECTION_STR.format(connection_keys)

        if echo is None:
            echo = database_config.echo

        super().__init__(connection_str, echo=echo)
