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
