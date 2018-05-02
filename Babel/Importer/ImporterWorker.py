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

import Babel.Logging.Logging as Logging
_module_logger = Logging.setup_logging('babel-worker')

# import logging
import os

from sidita import Worker

from ..Application.BabelApplication import BabelApplication
from ..Application.Arguments import Arguments

####################################################################################################

# _module_logger = logging.getLogger(__name__)

####################################################################################################

class ImportJob:

    ##############################################

    def __init__(self, application, path, shasum):

        self._application = application
        self.path = path
        self.shasum = shasum
        self.relative_path = self.path.relative_to(self.root_path)

    ##############################################

    @property
    def application(self):
        return self._application

    @property
    def document_database(self):
        return self._application.document_database

    @property
    def whoosh_database(self):
        return self._application.whoosh_database

    @property
    def root_path(self):
        return self._application.config.Path.DOCUMENT_ROOT_PATH

####################################################################################################

class ImporterWorker(Worker):

    _logger = _module_logger.getChild('ImporterWorker')

    ##############################################

    def __init__(self, worker_id):

        super().__init__(worker_id)

        self._application = None
        self._document_table = None
        self._root_path = None

    ##############################################

    def _init(self, data):

        self._logger.info('Init worker @{}\n{}'.format(self._worker_id, data))
        self._args = Arguments(**data)
        self._application = BabelApplication(args=self._args)
        self._document_table = self._application.document_database.document_table
        self._root_path = self._application.config.Path.DOCUMENT_ROOT_PATH

    ##############################################

    def on_task(self, task):

        try:
            action = task['action']
        except:
            action = None

        if action == 'init_worker':
            self._init(task['data'])
            return {
                'status': 'done',
            }

        elif action == 'import':
            self.import_file(task['path'])
            return {
                'status': 'done',
            }

        else:
            self._logger.error('Invalid action {}'.format(action))
            return {
                'status': 'error',
                'error_message': 'invalid action',
            }

    ##############################################

    def import_file(self, path):

        from .ImporterRegistry import ImporterRegistry, InvalidDocument

        if not path.is_relative_to(self._root_path):
            self._logger.error('File {} is not relative to root {}'.format(path, self._root_path))
            return

        # skip link ?
        if not path and os.path.lexists(str(path)):
            self._logger.error('File {} is a broken link'.format(path))
            return

        # skip empty file
        if not path.size:
            self._logger.error('File {} is empty'.format(path))
            return

        try:
            str(path).encode('utf8')
        except UnicodeEncodeError:
            # UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 84: surrogates not allowed
            # /home/from-salus/fabrice/home/ged/projets/lexique/Lexique380/Licence Lexique D\xe9tails.pdf
            self._logger.error("Unicode issue on file {}".format(str(path).encode('utf-8', 'surrogateescape')))
            return

        # self._logger.info("Look file {}".format(path))

        # Cases:
        #   - document is already registered (same path and checksum)
        #   - document is a duplicate (same checksum)
        #   - document was overwritten (same path)
        #   - new document

        # Store/Retrieve shasum from file's xattr
        if 'sha' not in path.xattr:
            shasum = path.shasum
            try:
                path.xattr['sha'] = shasum
            except PermissionError:
                self._logger.error("Permission issue for file {}".format(path))
        else:
            shasum = path.xattr['sha']

        job = ImportJob(self._application, path, shasum)

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
                # then log this file in the importer # Fixme: ???
                try:
                    document_row = ImporterRegistry.import_file(job)
                except InvalidDocument:
                    return
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
                    try:
                        document_row = ImporterRegistry.import_file(job)
                    except InvalidDocument:
                        return
