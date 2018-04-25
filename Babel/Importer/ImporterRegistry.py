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

# Fixme: use __init_subclass__, merge metaclass ?

####################################################################################################

import logging

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class ImporterRegistry(type):

    _logger =_module_logger.getChild('ImporterRegistry')

    __importers__ = {}

    ##############################################

    def __init__(cls, name, bases, namespace):

        type.__init__(cls, name, bases, namespace)

        if name != 'ImporterBase':
            for mime_type in cls.__mime_types__:
                if mime_type not in ImporterRegistry.__importers__:
                    ImporterRegistry.__importers__[mime_type] = cls
                else:
                    raise NameError("Mime Type {} for class {} is already registered".format(
                        mime_type, name))

    ##############################################

    @classmethod
    def import_file(cls, job):

        importer = cls.__importers__[job.path.mime_type]()
        return importer.import_file(job)

    ##############################################

    @classmethod
    def is_importable(cls, file_path):

        return file_path.mime_type in cls.__importers__

####################################################################################################

class InvalidDocument(NameError):
    pass

####################################################################################################

class ImporterBase(metaclass=ImporterRegistry):
    __mime_types__ = ()
