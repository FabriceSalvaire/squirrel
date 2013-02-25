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
import Babel.Config.Config as Config

####################################################################################################

class BabelApplication(ApplicationBase):

    _logger = logging.getLogger(__name__)
    
    ###############################################
    
    def __init__(self, args, **kwargs):
         
        super(BabelApplication, self).__init__(args=args, **kwargs)
        self._logger.debug(str(args) + ' ' + str(kwargs))

        self._make_user_directory()
        self._open_database()

    ###############################################
    
    def _make_user_directory(self):

        for directory in (Config.Path.config_directory,
                          Config.Path.data_directory):
            if not os.path.exists(directory):
                os.mkdir(directory)

    ###############################################
    
    def _open_database(self):

        self._file_database = FileDataBase(Config.DataBase.file_database)
        self._word_database = WordDataBase(Config.DataBase.word_database)
        self._word_document_database = WordDocumentDataBase(Config.DataBase.word_document_database)

####################################################################################################
#
# End
#
####################################################################################################
