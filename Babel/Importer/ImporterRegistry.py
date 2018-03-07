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

# Fixme: use __init_subclass__, merge metaclass ?

####################################################################################################

import logging

####################################################################################################

class ImporterRegistry(dict):

    ##############################################

    def __init__(self):

        super().__init__()

        # Fixme: global, ok ?
        self._document_database = None
        self._whoosh_database = None

    ##############################################

    @property
    def document_database(self):
        return self._document_database

    @document_database.setter
    def document_database(self, value):
        self._document_database = value

    @property
    def whoosh_database(self):
        return self._whoosh_database

    @whoosh_database.setter
    def whoosh_database(self, value):
        self._whoosh_database = value

    ##############################################

    def import_file(self, file_path):

        importer = self[file_path.mime_type]()
        return importer.import_file(self, file_path)

    ##############################################

    def is_importable(self, file_path):

        return file_path.mime_type in self

####################################################################################################

importer_registry = ImporterRegistry()

####################################################################################################

class ImporterMetaClass(type):

    ##############################################

    def __init__(cls, name, bases, namespace):

        # It is called just after cls creation in order to complete cls.

        # print('ImporterBase __init__:', cls, name, bases, namespace, sep='\n... ')

        type.__init__(cls, name, bases, namespace)
        if name != 'ImporterBase':
            for mime_type in cls.__mime_types__:
                if mime_type not in importer_registry:
                    importer_registry[mime_type] = cls
                else:
                    raise NameError("Mime Type {} for class {} is already registered".format(
                        mime_type, name))

####################################################################################################

class ImporterBase(metaclass=ImporterMetaClass):

    __mime_types__ = ()
