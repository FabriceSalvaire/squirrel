####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

from __future__ import print_function

####################################################################################################

import logging

####################################################################################################

class ImporterRegistry(dict):

    ##############################################

    def import_file(self, file_path):

        importer = self[file_path.mime_type]()
        importer.import_file(file_path)

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

class ImporterBase(object):

    __metaclass__ = ImporterMetaClass
    __mime_types__ = ()

####################################################################################################
# 
# End
# 
####################################################################################################
