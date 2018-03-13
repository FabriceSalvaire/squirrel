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

from .ImporterRegistry import ImporterBase
from Babel.Corpus.CorpusRegistry import CorpusRegistry
from Babel.Pdf.PdfDocument import PdfDocument, MupdfError
from Babel.Tools.Lazy import LazyInstantiator

####################################################################################################

class PdfImporter(ImporterBase):

    __mime_types__ = ('application/pdf',)

    _logger = logging.getLogger(__name__)

    ##############################################

    def import_file(self, job):

        # PdfMetaDataExtractor

        try:
            pdf_document = PdfDocument(job.path)
        except MupdfError:
            return

        whoosh_database = job.whoosh_database
        text = pdf_document.text()
        whoosh_database.index(shasum=job.shasum, content=text)

        # Fixme: registry
        document_table = job.document_database.document_table
        word_table = job.document_database.word_table

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
        words, unknown_words = self.main_words(pdf_document, last_page)

        if len(words) > len(unknown_words):
            document_row.indexed_until = last_page +1 # from 1
            if last_page == pdf_document.number_of_pages -1:
                document_row.indexation_status = 'full'
            else:
                document_row.indexation_status = 'partial'
            document_row.language = 'en' # Fixme: other language !!!
            for word_count in words:
                word_table.add_new_row(document=document_row,
                                       language=1, # en
                                       word=word_count.word, count=word_count.count, rank=word_count.rank)
            for word_count in unknown_words:
                word_table.add_new_row(document=document_row,
                                       language=0,
                                       word=word_count.word, count=word_count.count, rank=word_count.rank)
            word_table.commit()
        else:
            self._logger.warning("Unknown language for %s", job.path)
            document_row.indexed_until = last_page +1 # from 1
            document_row.indexation_status = 'unknown language'
            document_row.language = '?'
        document_row.update_indexation_date()

        document_table.add(document_row, commit=False)

        return document_row

    ##############################################

    def main_words(self, pdf_document, last_page=None, minimum_count=5, minimum_length=3):

        corpus_registry = CorpusRegistry()

        words = []
        unknown_words = []
        for word_count in pdf_document.collect_document_words(last_page):
            if word_count.count >= minimum_count and len(word_count.word) >= minimum_length:
                corpus_entry = corpus_registry[word_count.word]
                if corpus_entry is not None:
                    word_entry = corpus_entry.most_probable_language
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

        return words, unknown_words
