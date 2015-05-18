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

# Fixme: move elsewhere? not an importer or FileSystem

####################################################################################################

from Babel.FileSystem.File import Directory
from Babel.Pdf.PdfDocument import PdfDocument
from Babel.Tools.Container import Ring

####################################################################################################

class DocumentItem(object):

    ##############################################

    def __init__(self, path):

        self._path = path
        self._selected = False

    ##############################################

    def __repr__(self):

        return 'DocumentItem ' + str(self._path)
    
    ##############################################

    @property
    def path(self):
        return self._path

    ##############################################

    @property
    def selected(self):
        return self._selected

    ##############################################

    @selected.setter
    def selected(self, value):
        self._selected = value

####################################################################################################

class PdfDocumentItem(DocumentItem):

    # Fixme: purpose
    
    ##############################################

    def __init__(self, path):

        super(PdfDocumentItem, self).__init__(path)

        self._document = None

        # self._cover_page = self._pdf_document[0]

    ##############################################
    
    @property
    def document(self):

        if self._document is None:
            self._document = PdfDocument(self._path)
        return self._document

####################################################################################################

class DocumentDirectory(Ring):

    __importable_mime_types__ = ('application/pdf',
                                )

    __classes__ = {'application/pdf':PdfDocumentItem,
                  }
    
    ##############################################

    def __init__(self, path, importable_mime_types=None):

        super(DocumentDirectory, self).__init__()

        self._path = Directory(path)
        if importable_mime_types is None:
            self._importable_mime_types = self.__importable_mime_types__
        else:
            self._importable_mime_types = importable_mime_types
       
        self._open_directory()

    ##############################################

    @property
    def path(self):
        return self._path

    ##############################################

    def _is_file_importable(self, file_path):

        return file_path.mime_type in self._importable_mime_types

    ##############################################

    def _open_directory(self):

        file_paths = sorted(self._path.iter_files(), key=lambda x: str(x.path))
        for file_path in file_paths:
            if self._is_file_importable(file_path):
                document_class = self.__classes__[file_path.mime_type]
                document = document_class(file_path)
                self.add(document)

    ##############################################

    def find_path(self, file_path):

        for document in self:
            if file_path == document.path:
                return document
        return None

    ##############################################

    def delete_path(self, file_path):

        for i, document in enumerate(self):
            if file_path == document.path:
                self.delete_index(i) # return
                return True
        return False

####################################################################################################
# 
# End
# 
####################################################################################################
