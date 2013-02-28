####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

###################################################################################################

import logging
import os

####################################################################################################

from Babel.Application.ApplicationBase import ApplicationBase
from Babel.DataBase.FileDataBase import FileDataBase
from Babel.DataBase.WordDataBase import WordDataBase
from Babel.DataBase.WordDocumentDataBase import WordDocumentDataBase
from Babel.FileSystem.File import Directory, File
from Babel.Tools.Singleton import MetaSingleton
import Babel.Config.Config as Config

####################################################################################################

class BabelApplication(ApplicationBase):

    # __metaclass__ = MetaSingleton

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

        self.file_database = FileDataBase(Config.DataBase.file_database)
        self.word_database = WordDataBase(Config.DataBase.word_database)
        self.word_document_database = WordDocumentDataBase(Config.DataBase.word_document_database)

    ###############################################
    
    def import_path(self, path):

        import_session = self._importer.new_session()
        import_session.import_path(Directory(path))

####################################################################################################
#
# End
#
####################################################################################################
