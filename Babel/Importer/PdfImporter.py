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

import logging

####################################################################################################

from Babel.Corpus.LanguageId import LanguageId
from Babel.Pdf.PdfDocument import PdfDocument, MupdfError
# from Babel.Tools.Lazy import LazyInstantiator
from .ImporterRegistry import ImporterBase, InvalidDocument

####################################################################################################

class PdfImporter(ImporterBase):

    __mime_types__ = ('application/pdf',)

    _logger = logging.getLogger(__name__)

    ##############################################

    def import_file(self, job):

        # PdfMetaDataExtractor

        if not PdfDocument.check_magic_number(job.path):
            message = 'Invalid Magic Number for PDF Document {}'.format(job.path)
            self._logger.error(message)
            raise InvalidDocument(message)

        try:
            pdf_document = PdfDocument(job.path)
        except MupdfError as exception:
            raise InvalidDocument() # exception. ...

        whoosh_database = job.whoosh_database
        text = pdf_document.text()
        whoosh_database.index(shasum=job.shasum, content=text, async_index=True)
        # whoosh_database.async_index(shasum=job.shasum, content=text)

        # Fixme: registry
        document_database = job.document_database
        document_table = document_database.document_table

        document_row = document_table.new_row(job)

        document_row.number_of_pages = pdf_document.number_of_pages

        pdf_metadata = pdf_document.metadata
        # ('Title', 'Subject', 'Author', 'Creator', 'Producer', 'CreationDate', 'ModDate')
        document_row.title = pdf_metadata['Title']
        document_row.author = pdf_metadata['Author']

        number_of_pages_threshold = 10
        if pdf_document.number_of_pages > number_of_pages_threshold:
            last_page = number_of_pages_threshold
        else:
            last_page = pdf_document.number_of_pages -1
        self._get_main_words(pdf_document, last_page)

        document_row.indexed_until = last_page +1 # from 1

        if len(self._resolved_words) > len(self._unknown_words):
            if last_page == pdf_document.number_of_pages -1:
                document_row.indexation_status = 'full'
            else:
                document_row.indexation_status = 'partial'
            document_row.language = self._document_words.dominant_language()
        else:
            self._logger.warning("Unknown language for %s", job.path)
            document_row.indexation_status = 'unknown language'
            document_row.language = LanguageId.unknown
        document_row.update_indexation_date()

        document_table.add(document_row, commit=True)

        words = self._resolved_words + self._unknown_words;
        document_database.add_words_for_document(document_row, words)

        return document_row

    ##############################################

    def _get_main_words(self, pdf_document, last_page=None, minimum_count=5, minimum_length=3):

        self._document_words = pdf_document.collect_document_words(last_page)

        words = []
        unknown_words = []
        for word_count in self._document_words:
            if word_count.count >= minimum_count and len(word_count.word) >= minimum_length:
                word_entry = word_count.word_entry
                if word_entry is not None:
                    if word_entry.is_noun:
                        words.append(word_count)
                else:
                    unknown_words.append(word_count)

        # if len(words) > len(unknown_words):
        #     for word_count in words:
        #         print('%6u' % word_count.count, word_count.word)
        #     for word_count in unknown_words:
        #         print('Unknown word %6u' % word_count.count, word_count.word)

        # Fixme: filter work like 'xxxxx'

        self._resolved_words = words
        self._unknown_words = unknown_words
