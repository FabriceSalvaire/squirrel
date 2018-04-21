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

__all__ = [
    'DocumentDirectory',
]

####################################################################################################

# Fixme:
#   only used in PdfBrowserMainWindow
#   Not UI component
#   move elsewhere? not an importer or FileSystem

####################################################################################################

from Babel.FileSystem.File import Directory
from Babel.Pdf.PdfDocument import PdfDocument
from Babel.Tools.Container import Ring

####################################################################################################

class DocumentItem:

    ##############################################

    def __init__(self, path):

        self._path = path
        self._selected = False

    ##############################################

    def __repr__(self):
        return self.__class__.__name__ + ' ' + str(self._path)

    ##############################################

    @property
    def path(self):
        return self._path

    ##############################################

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value

####################################################################################################

class PdfDocumentItem(DocumentItem):

    # Fixme: purpose ?

    ##############################################

    def __init__(self, path):

        super().__init__(path)

        self._document = None # lazy

        # self._cover_page = self._pdf_document[0]

    ##############################################

    @property
    def document(self):

        if self._document is None:
            self._document = PdfDocument(self._path)
        return self._document

####################################################################################################

class DocumentList(Ring):

    ##############################################

    # Unused
    #
    # def find_path(self, file_path):
    #     # find_document_by_path
    #     for document in self:
    #         if file_path == document.path:
    #             return document
    #     return None

    ##############################################

    def rotate_to_path(self, path):

        # self.find(PdfDocumentItem(path))

        for i, document in enumerate(self):
            if path == document.path:
                self.current_index = i
                break

    ##############################################

    def delete_path(self, file_path):

        # delete_document_by_path

        for i, document in enumerate(self):
            if file_path == document.path:
                self.delete_index(i) # return
                return True
        return False

####################################################################################################

class DocumentDirectory(DocumentList):

    __importable_mime_types__ = (
        'application/pdf',
    )

    __classes__ = {
        'application/pdf':PdfDocumentItem,
    }

    ##############################################

    def __init__(self, path, importable_mime_types=None):

        super().__init__()

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

        # Fixme: to func
        file_paths = [path for path in self._path.iter_files() if self._is_file_importable(path)]
        file_paths.sort(key=lambda path: str(path))
        for file_path in file_paths:
            cls = self.__classes__[file_path.mime_type]
            document = cls(file_path)
            self.add(document)
