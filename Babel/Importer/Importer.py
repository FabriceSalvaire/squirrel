####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################
#
#                                              Audit
#
# - 25/02/2013 Fabrice
#   use prefix in file database so as to be portable accross filesystem
#   path.relative_to(prefix)
#
####################################################################################################

####################################################################################################

import logging

####################################################################################################

# from Babel.Application.BabelApplication import BabelApplication
from Babel.FileSystem.File import Path, Directory, File
from Babel.Importer.ImporterRegistry import importer_registry

####################################################################################################

class Importer(object):

    _logger = logging.getLogger(__name__)

    importable_mime_types = ('application/pdf',
                             )

    ##############################################

    def __init__(self, application):

        self._application = application
        # application = BabelApplication()

    ##############################################

    def new_session(self):

        return ImportSession(self)

####################################################################################################

class ImportSession(object):

    _logger = logging.getLogger(__name__)

    ##############################################

    def __init__(self, importer):

        self._importer = importer

    ##############################################

    def import_path(self, path):

        path = Path(path).real_path()
        if path.is_directory():
            self.import_recursively_path(Directory(path))
        else:
            self.import_file(File(path))

    ##############################################

    def import_recursively_path(self, path):

        for file_path in path.walk_files():
            if self.is_file_importable(file_path):
                self.import_file(file_path)
            else:
                self._logger.info("File %s is not importable" % (file_path))

    ##############################################

    def is_file_importable(self, file_path):

        return file_path.mime_type in self._importer.importable_mime_types

    ##############################################

    def import_file(self, file_path):
        
        file_table = self._importer._application.file_database.file_table
        query = file_table.select_by(path=str(file_path), shasum=file_path.shasum)
        if query.count():
            self._logger.info("File %s is already imported" % (file_path))
            # then do nothing
        else:
            query = file_table.select_by(shasum=file_path.shasum)
            if query.count():
                file_paths = ' '.join([row.path for row in query.all()])
                self._logger.info("File %s is a duplicate of %s" % (file_path, file_paths))
                # then log this file in the import session
            else:
                query = file_table.select_by(path=str(file_path))
                if query.count():
                    self._logger.info("File %s was overwritten" % (file_path))
                    # then update data
                    file_row = query.one()
                    file_row.update(file_path)
                    file_table.commit()
                else:
                    file_table.add(file_path)
                    file_table.commit()
                    #try:
                    importer_registry.import_file(file_path)
                    #except:
                    #    pass

####################################################################################################
# 
# End
# 
####################################################################################################
