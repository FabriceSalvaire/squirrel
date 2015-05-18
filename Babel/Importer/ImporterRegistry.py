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

class ImporterRegistry(dict):

    ##############################################

    def import_file(self, document_table, file_path):

        importer = self[file_path.mime_type]()
        return importer.import_file(document_table, file_path)

    ##############################################

    def is_importable(self, file_path):

        return file_path.mime_type in self
    
####################################################################################################

importer_registry = ImporterRegistry()

####################################################################################################

class ImporterMetaClass(type):

    ##############################################

    def __init__(cls, class_name, super_classes, class_attribute_dict):

        # It is called just after cls creation in order to complete cls.

        # print('ImporterBase __init__:', cls, class_name, super_classes, class_attribute_dict, sep='\n... ')

        type.__init__(cls, class_name, super_classes, class_attribute_dict)
        if class_name != 'ImporterBase':
            for mime_type in cls.__mime_types__:
                if mime_type not in importer_registry:
                    importer_registry[mime_type] = cls
                else:
                    raise NameError("Mime Type %s for class %s is already registered" %
                                    (mime_type, class_name))

####################################################################################################

class ImporterBase(object, metaclass=ImporterMetaClass):

    __mime_types__ = ()

####################################################################################################
# 
# End
# 
####################################################################################################
