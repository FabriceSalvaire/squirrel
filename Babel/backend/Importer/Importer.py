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
import asyncio
import logging
import os

from sidita import TaskQueue
from sidita.Units import u_MB

from ..DataBase.DocumentDataBase.LogTable import ImporterStatus
from ..FileSystem.File import Path, Directory

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Importer:

    _logger = _module_logger.getChild('Importer')

    ##############################################

    def __init__(self, application):

        self._application = application
        self._root_path = self._application.config.Path.DOCUMENT_ROOT_PATH

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
            self._application,
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

    def __init__(self, application, path, **kwargs):

        super().__init__(
            # python_path=Path(__file__).resolve().parent,
            worker_module='Babel.backend.Importer.ImporterWorker',
            worker_cls='ImporterWorker',
            **kwargs
        )

        self._application = application
        self._path = path

        self._root_path = self._application.config.Path.DOCUMENT_ROOT_PATH
        self._importer_log_table = self._application.document_database.importer_log_table

    ##############################################

    def _log(self, task_metadata, status):

        path = task_metadata.task['path'].relative_to(self._root_path)

        self._importer_log_table.add_new_row(
            path=str(path),
            date=task_metadata.dispatch_date,
            time=task_metadata.task_time_s, # doesn't remove waiting
            status=status,
        )
        # self._importer_log_table.commit() # freeze event loop

    ##############################################

    def run(self):

        auxiliary_coroutines=[
            self._commit()
        ]

        super().run(auxiliary_coroutines)

    ##############################################

    async def _commit(self):

        while self.is_running:
            self._commit_sleep_future = asyncio.ensure_future(asyncio.sleep(60))
            await self._commit_sleep_future
            self._logger.info('commit')
            self._importer_log_table.commit()

        self._logger.info('Exit commit coroutine')
        # self._importer_log_table.commit()

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

    def on_all_consumer_stopped(self):

        super().on_all_consumer_stopped()
        self._commit_sleep_future.cancel() # will raise CancelledError on run_until_complete

    ##############################################

    def on_closed_event_loop(self, task_consumers):

        self._logger.info('last commit')
        self._importer_log_table.commit()

        super().on_closed_event_loop(task_consumers)

    ##############################################

    def on_task_submitted(self, task_metadata):
        super().on_task_submitted(task_metadata)

    ##############################################

    def on_task_sent(self, task_metadata):
        super().on_task_sent(task_metadata)

    ##############################################

    def on_result(self, task_metadata):
        super().on_result(task_metadata)
        self._log(task_metadata, ImporterStatus.COMPLETED)

    ##############################################

    def on_timeout_error(self, task_metadata):
        self._log(task_metadata, ImporterStatus.TIMEOUT)

    ##############################################

    def on_stream_error(self, task_metadata):
        self._log(task_metadata, ImporterStatus.CRASHED)
