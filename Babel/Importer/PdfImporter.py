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

from .ImporterRegistry import ImporterBase
from Babel.Pdf.PdfDocument import PdfDocument

####################################################################################################

from Babel.Lexique.BritishNationalCorpus import BritishNationalCorpusDataBase
_bnc_database = BritishNationalCorpusDataBase()
_bnc_word_table = _bnc_database.word_table

####################################################################################################

class PdfImporter(ImporterBase):

    __mime_types__ = ('application/pdf',)

    _logger = logging.getLogger(__name__)

    ##############################################

    def import_file(self, document_table, file_path):
        
        pdf_document = PdfDocument(file_path)
        # PdfMetaDataExtractor
        
        document_row = document_table.new_row(file_path)

        document_row.number_of_pages = pdf_document.number_of_pages
        
        pdf_metadata = pdf_document.metadata
        # ('Title', 'Subject', 'Author', 'Creator', 'Producer', 'CreationDate', 'ModDate')}
        document_row.title = pdf_metadata['Title']
        document_row.author = pdf_metadata['Author']

        print(file_path)
        # self.main_words(pdf_document)
        
        document_table.add(document_row, commit=False)
        
        return document_row

    ##############################################

    def main_words(self, pdf_document, minimum_count=5, minimum_length=3):

        words = []
        # Fixme: to iterator ?
        for word_count in pdf_document.words:
            print(word_count)
            # if word_count.count >= minimum_count and len(word_count.word) >= minimum_length:
            #     word_rows = _bnc_word_table.filter_by(word=word_count.word).all()
            #     if word_rows:
            #         for word_row in word_rows: 
            #             if _bnc_database.is_noun(word_row):
            #                 tag = _bnc_database.part_of_speech_tag_from_id(word_row.part_of_speech_tag_id)
            #                 print('%6u' % word_count.count, word_count.word, tag)
            #                 words.append(word_count)
            #                 break
            #     else:
            #         print('Unknown word %6u' % word_count.count, word_count.word)
            #         words.append(word_count)
                
####################################################################################################
# 
# End
# 
####################################################################################################
