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

from datetime import timedelta
import logging
import os

from sidita import TaskQueue
from sidita.Units import u_MB

from ..FileSystem.File import Path, Directory

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Importer:

    _logger = _module_logger.getChild('Importer')

    ##############################################

    def __init__(self, application):

        self._application = application
        self._document_table = self._application.document_database.document_table
        self._root_path = self._application.config.Path.DOCUMENT_ROOT_PATH

    ##############################################

    @property
    def application(self):
        return self._application

    ##############################################

    def import_path(self, path=None):

        if path is None:
            path =self._root_path

        path = Path(path).real_path()
        if path.is_directory():
            self.import_recursively_path(Directory(path))
        else:
            # Fixme:
            raise NotImplementedError
            # self.import_file(File(path))

    ##############################################

    def import_recursively_path(self, path):

        init_worker = dict(
            config=str(self._application.args.config),
        )

        number_of_workers = os.cpu_count()

        task_queue = ImporterTaskQueue(
            path,
            init_worker=init_worker,
            max_queue_size=number_of_workers*5,
            number_of_workers = number_of_workers,
            max_memory=128@u_MB,
            memory_check_interval=timedelta(minutes=2),
            task_timeout=timedelta(minutes=5),
        )
        task_queue.run()

####################################################################################################

class ImporterTaskQueue(TaskQueue):

    _logger = _module_logger.getChild('ImporterTaskQueue')

    ##############################################

    def __init__(self, path, **kwargs):

        super().__init__(
            # python_path=Path(__file__).resolve().parent,
            worker_module='Babel.Importer.ImporterWorker',
            worker_cls='ImporterWorker',
            **kwargs
        )

        self._path = path

    ##############################################

    async def task_producer(self):

        from .ImporterRegistry import ImporterRegistry

        for file_path in self._path.walk_files():
            if ImporterRegistry.is_importable(file_path):
                task = {
                    'action': 'import',
                    'path': file_path,
                }
                await self.submit(task)
            # else:
            #     self._logger.info("File {} is not importable".format(file_path))

        await self.send_stop()

    ##############################################

    def on_task_submitted(self, task_metadata):

        super().on_task_submitted(task_metadata)

    ##############################################

    def on_task_sent(self, task_metadata):

        super().on_task_sent(task_metadata)

    ##############################################

    def on_result(self, task_metadata):

        super().on_result(task_metadata)

    ##############################################

    def on_timeout_error(self, task_metadata):

        pass

    ##############################################

    def on_stream_error(self, task_metadata):

        pass
