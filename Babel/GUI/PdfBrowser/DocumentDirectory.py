####################################################################################################
# 
# Babel - A Bibliography Manager
# Copyright (C) Salvaire Fabrice 2014
# 
####################################################################################################

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

    @property
    def selected(self):
        return self._selected

    ##############################################

    @selected.setter
    def selected(self, value):
        self._selected = value

####################################################################################################

class PdfDocumentItem(DocumentItem):

    ##############################################

    def __init__(self, path):

        super(PdfDocumentItem, self).__init__(path)

        self._pdf_document = None
        self._cover_page = None
        self._image_cache = {}

    ##############################################

    def load(self, width=None, height=None, resolution=150):

        if self._pdf_document is None:
            self._pdf_document = PdfDocument(self._path)
            self._cover_page = self._pdf_document[0]

        key = '{}-{}-{}'.format(width, height, resolution)
        if key in self._image_cache:
            return self._image_cache[key]
        else:
            image = self._cover_page.to_pixmap(resolution=resolution, width=width, height=height)
            self._image_cache[key] = image
            return image

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

        for file_path in self._path.iter_files():
            if self._is_file_importable(file_path):
                document_class = self.__classes__[file_path.mime_type]
                document = document_class(file_path)
                self.add(document)

####################################################################################################
# 
# End
# 
####################################################################################################
