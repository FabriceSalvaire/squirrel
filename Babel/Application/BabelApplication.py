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

###################################################################################################

import logging
import os

####################################################################################################

# from Babel.DataBase.WordDataBase import WordDataBase
# from Babel.Tools.Singleton import SingletonMetaClass
from Babel.Application.ApplicationBase import ApplicationBase
from Babel.DataBase.DocumentDataBase import DocumentSqliteDataBase
from Babel.FileSystem.File import Directory
import Babel.Config.Config as Config

####################################################################################################

class BabelApplication(ApplicationBase):

    # __metaclass__ = SingletonMetaClass

    _logger = logging.getLogger(__name__)
    
    ###############################################
    
    def __init__(self, args, **kwargs):
         
        super(BabelApplication, self).__init__(args=args, **kwargs)
        self._logger.debug(str(args) + ' ' + str(kwargs))

        self._make_user_directory()
        self._open_database()

        from Babel.Importer.Importer import Importer
        self._importer = Importer(self)

    ###############################################
    
    def _make_user_directory(self):

        for directory in (Config.Path.config_directory,
                          Config.Path.data_directory):
            if not os.path.exists(directory):
                os.mkdir(directory)

    ###############################################
    
    def _open_database(self):

        self.document_database = DocumentSqliteDataBase(Config.DataBase.document_database)
        # self.word_database = WordDataBase(Config.DataBase.word_database)

    ###############################################
    
    def import_path(self, path):

        import_session = self._importer.new_session()
        import_session.import_path(Directory(path))

####################################################################################################
#
# End
#
####################################################################################################
