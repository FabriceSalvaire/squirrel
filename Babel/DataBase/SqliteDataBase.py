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

import logging
import os
import stat

####################################################################################################

from .DataBase import DataBase

####################################################################################################

class SqliteDataBase(DataBase):

    _logger = logging.getLogger(__name__)

    ##############################################
    
    def __init__(self, filename, echo=False):

        self._logger.debug("Open SQLite Database %s" % (filename))
        
        self._filename = filename

        self._created = not os.path.exists(self._filename)
        self._before_alter_backuped = False

        super(SqliteDataBase, self).__init__(connection_string="sqlite:///" + self._filename,
                                             echo=echo)

    ###############################################

    @property
    def filename(self):
        return self._filename

    ###############################################

    @property
    def dirname(self):
        return  os.path.dirname(self._filename)

    ##############################################
    
    def create(self):

        # Fixme: it don't check if there is any table

        if self._created:
            self._logger.info("Create DataBase %s" % (self._filename))
            self._declarative_base_class.metadata.create_all(bind=self._engine)
            # Set POSIX permission, user needs the right privilege to achieve it
            os.chmod(self._filename, stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IWGRP)
        return self._created

    ###############################################
    
    def journal_exists(self):

        # Fixme: New extension?
        journal_filename = self._filename + '-journal'
        return os.path.exists(journal_filename)

    ###############################################
    
    def alter_table(self, table_name, columns_statements):
        
        # Fixme: look at
        # http://docs.sqlalchemy.org/en/rel_0_8/core/metadata.html#sqlalchemy.schema.Table
        # extend_existing=True

        table_columns = self.table_columns(table_name)
        for column, alter_table_statement in columns_statements:
            if column not in table_columns:
                # self.backup_file(suffix='.before-alter')
                sql_statement = 'ALTER TABLE %s ADD COLUMN ' % table_name + column + ' ' + alter_table_statement
                self._logger.info(sql_statement)
                self.session.execute(sql_statement)

####################################################################################################
#
# End
#
####################################################################################################
