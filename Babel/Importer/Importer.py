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

####################################################################################################

# from Babel.Application.BabelApplication import BabelApplication

from Babel.FileSystem.File import Path, Directory, File
from Babel.Importer.ImporterRegistry import ImporterRegistry

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Importer:

    ##############################################

    def __init__(self, application):

        self._application = application
        # application = BabelApplication()

    ##############################################

    @property
    def application(self):
        return self._application

    ##############################################

    def new_session(self):
        return ImportSession(self)

####################################################################################################

class ImportJob:

    ##############################################

    def __init__(self, session, path, shasum):

        self.session = session
        self.path = path
        self.shasum = shasum
        self.relative_path = self.path.relative_to(self.root_path)

    ##############################################

    @property
    def application(self):
        return self.session.application

    @property
    def document_database(self):
        return self.application.document_database

    @property
    def whoosh_database(self):
        return self.application.whoosh_database

    @property
    def root_path(self):
        return self.application.config.document_root_path

####################################################################################################

class ImportSession:

    # Fixme: purpose ?

    _logger = _module_logger.getChild('ImportSession')

    ##############################################

    def __init__(self, importer):

        self._importer = importer
        self._document_table = self.application.document_database.document_table
        self._root_path = self.application.config.document_root_path

    ##############################################

    @property
    def application(self):
        return self._importer.application

    ##############################################

    def import_path(self, path=None):

        if path is None:
            path =self._root_path

        path = Path(path).real_path()
        if path.is_directory():
            self.import_recursively_path(Directory(path))
        else:
            self.import_file(File(path))

    ##############################################

    def import_recursively_path(self, path):

        for file_path in path.walk_files():
            if ImporterRegistry.is_importable(file_path):
                self.import_file(file_path)
            # else:
            #     self._logger.info("File {} is not importable".format(file_path))

    ##############################################

    def import_file(self, path):

        # Fixme: MuPDF exception
        if str(job.relative_path) in (
                'racine/science-appliques/electronique/fournisseurs/datasheet/introduction-68hc11.pdf',
                'racine/science-appliques/electronique/a-trier/sensors/accelerometer-magnetometer/SENSPRODCAT.pdf',
                'racine/technologies/construction-batiment/electricité/NF-C15-100.pdf',
        ):
            return

        if not path.is_relative_to(self._root_path):
            self._logger.error("File {} is not relative to root {}".format(path, self._root_path))
            return

        # Cases:
        #   - document is already registered (same path and checksum)
        #   - document is a duplicate (same checksum)
        #   - document was overwritten (same path)
        #   - new document

        # Store/Retrieve shasum from file's xattr
        if 'sha' not in path.xattr:
            shasum = path.shasum
            path.xattr['sha'] = shasum
        else:
            shasum = path.xattr['sha']

        job = ImportJob(self, path, shasum)

        query = self._document_table.filter_by(path=str(job.relative_path), shasum=shasum)
        if query.count():
            self._logger.info("File {} is already imported".format(path))
            # then do nothing
            # Fixme: update case
        else:
            query = self._document_table.filter_by(shasum=shasum)
            if query.count():
                duplicates = query.all()
                paths = ' '.join([str(document_row.path) for document_row in duplicates])
                self._logger.info("File {} is a duplicate of {}".format(path, paths))
                # then log this file in the import session # Fixme: ???
                document_row = ImporterRegistry.import_file(job)
                document_row.has_duplicate = True
                for document_row in duplicates:
                    document_row.has_duplicate = True
            else:
                query = self._document_table.filter_by(path=str(job.relative_path))
                if query.count():
                    self._logger.info("File {} was overwritten".format(path))
                    # then update shasum
                    document_row = query.one()
                    document_row.update_shasum(path)
                else:
                    self._logger.info("Add file {}".format(path))
                    document_row = ImporterRegistry.import_file(job)
            self._document_table.commit()
