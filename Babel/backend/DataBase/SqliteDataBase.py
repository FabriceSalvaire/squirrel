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
import stat
from pathlib import Path

from .DataBase import DataBase

####################################################################################################

class SqliteDataBase(DataBase):

    _logger = logging.getLogger(__name__)

    ##############################################

    def __init__(self, filename, echo=False):

        self._filename = Path(str(filename))

        self._logger.debug("Open SQLite Database {}".format(self._filename))

        self._created = self._filename.exists()
        self._before_alter_backuped = False

        super().__init__(
            connection_string='sqlite:///{}'.format(self._filename),
            echo=echo,
        )

    ###############################################

    @property
    def filename(self):
        return self._filename

    @property
    def dirname(self):
        return self._filename.parent

    ##############################################

    def create(self):

        # Fixme: it don't check if there is any table

        if not self._created:
            self._logger.info("Create DataBase {}".format(self._filename))
            self._declarative_base_cls.metadata.create_all(bind=self._engine)
            # Set POSIX permission, user needs the right privilege to achieve it
            self._filename.chmod(stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IWGRP)
            self._created = True
        return self._created

    ###############################################

    def journal_exists(self):

        # Fixme: New extension ?
        journal_filename = self._filename + '-journal'
        return Path(journal_filename).exists()
