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

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Importer(object):

    ##############################################

    def __init__(self, application):

        self._application = application
        # application = BabelApplication()

    ##############################################

    def new_session(self):

        return ImportSession(self)

####################################################################################################

class ImportSession(object):

    # fixme: purpose ?

    _logger = _module_logger.getChild('ImportSession')
   
    ##############################################

    def __init__(self, importer):

        self._importer = importer
        document_database = self._importer._application.document_database
        self._document_table = document_database.document_table
        
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
            if importer_registry.is_importable(file_path):
                self.import_file(file_path)
            else:
                self._logger.info("File %s is not importable" % (file_path))

    ##############################################

    def import_file(self, file_path):

        # Cases:
        #   - document is already registered (same path and checksum)
        #   - document is a duplicate (same checksum)
        #   - document was overwritten (same path)
        #   - new document
        
        query = self._document_table.filter_by(path=str(file_path), shasum=file_path.shasum)
        if query.count():
            self._logger.info("File %s is already imported" % (file_path))
            # then do nothing
        else:
            query = self._document_table.filter_by(shasum=file_path.shasum)
            if query.count():
                duplicates = query.all()
                file_paths = ' '.join([str(document_row.path) for document_row in duplicates])
                self._logger.info("File %s is a duplicate of %s", file_path, file_paths)
                # then log this file in the import session # Fixme: ???
                document_row = importer_registry.import_file(self._document_table, file_path)
                document_row.has_duplicate = True
                for document_row in duplicates:
                    document_row.has_duplicate = True
            else:
                query = self._document_table.filter_by(path=str(file_path))
                if query.count():
                    self._logger.info("File %s was overwritten", file_path)
                    # then update shasum
                    document_row = query.one()
                    document_row.update_shasum(file_path)
                else:
                    self._logger.info("Add file %s", file_path)
                    # Fixme: self._document_table, via importer_registry ?
                    document_row = importer_registry.import_file(self._document_table, file_path)
            self._document_table.commit()
                
####################################################################################################
# 
# End
# 
####################################################################################################
