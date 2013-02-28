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

import codecs
import logging

####################################################################################################

from Babel.Importer.ImporterRegistry import ImporterBase
from Babel.Pdf.PdfDocument import PdfDocument

####################################################################################################

class PdfImporter(ImporterBase):

    __mime_types__ = ('application/pdf',)

    _logger = logging.getLogger(__name__)

    ##############################################

    def import_file(self, file_path):

        self._path = file_path
        self._pdf_document = PdfDocument(self._path) # Fixme: has path
        self._pdf_metadata = self._pdf_document.metadata
        print 'Title:', self._pdf_metadata['Title']

#    ##############################################
#
#    def _get_metadata(self):
#
#        self._pdf_metadata = self. _pdf_document.metadata
#        # self._pdf_document.number_of_pages
#        # {key:self._pdf_metadata[key]
#        #  for key in
#        #  ('Title', 'Subject', 'Author', 'Creator', 'Producer', 'CreationDate', 'ModDate')}
#        # pdf_metadata.metadata

####################################################################################################
# 
# End
# 
####################################################################################################
