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

###################################################################################################

import logging

####################################################################################################

# from Babel.backend.Database.WordDatabase import WordDatabase
# from Babel.backend.Tools.Singleton import SingletonMetaClass

from ..Application.ApplicationBase import ApplicationBase
from Babel.config.ConfigFile import ConfigFile
from Babel.backend.Database import DocumentDatabase
from Babel.backend.Database.WhooshDatabase import WhooshDatabase
from Babel.backend.FileSystem.File import Directory

####################################################################################################

class BabelApplication(ApplicationBase):

    # __metaclass__ = SingletonMetaClass

    _logger = logging.getLogger(__name__)

    ###############################################

    def __init__(self, args, **kwargs):

        super(BabelApplication, self).__init__(args=args, **kwargs)
        self._logger.debug(str(args) + ' ' + str(kwargs))

        # Config.make_user_directory()
        self._config = ConfigFile(args.config)
        self._open_database()

        self._importer = None

        from Babel.backend.Search import Searcher
        self._searcher = Searcher(self)

    ##############################################

    @property
    def config(self):
        return self._config

    @property
    def document_database(self):
        return self._document_database

    @property
    def whoosh_database(self):
        return self._whoosh_database

    ###############################################

    def _open_database(self):
        self._document_database = DocumentDatabase.open_database(self._config.Database)
        self._whoosh_database = WhooshDatabase(self._config.Database.whoosh_database())

    ###############################################

    def index_all(self, args):

        # Fixme: name ??? update_index, index

        self._logger.info('Index {}'.format(self._config.Path.DOCUMENT_ROOT_PATH))

        if self._importer is None:
            from Babel.backend.Importer.Importer import Importer
            self._importer = Importer(self)

        self._importer.import_path()

    ##############################################

    def console_search(self, args):
        self._searcher.console_search(args)

    ##############################################

    def console_corpus_search(self, args):
        from Babel.backend.Corpus.ConsoleSearch import console_search
        console_search(args)

    ##############################################

    def console_database_statistics(self, args):
        from Babel.backend.DatabaseStatistics import console_database_statistics
        console_database_statistics(self, args)
