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

from .Database import Database

####################################################################################################

class ServerDatabase(Database):

    _logger = logging.getLogger(__name__)

    CONNECTION_STRING = "{0.driver}://{0.user_name}:{0.password}@{0.hostname}/{0.database}"

    ###############################################

    def __init__(self, database_config, echo=None):

        connection_string = self.CONNECTION_STRING.format(connection_keys)

        self._logger.debug('Open Database {}'.format(connection_str))

        if echo is None:
            echo = database_config.echo

        super().__init__(connection_str, echo=echo)

    ##############################################

    def create(self):

        # Fixme: it don't check if there is any table

        if not self._created:
            self._logger.info('Create Database')
            self._declarative_base_cls.metadata.create_all(bind=self._engine)
            self._created = True
        return self._created
