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
from Babel.Pdf.PdfDocument import PdfDocument, MupdfError

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

        # PdfMetaDataExtractor
        
        try:
            pdf_document = PdfDocument(file_path)
        except MupdfError:
            return
            
        document_row = document_table.new_row(file_path)

        document_row.number_of_pages = pdf_document.number_of_pages
        
        pdf_metadata = pdf_document.metadata
        # ('Title', 'Subject', 'Author', 'Creator', 'Producer', 'CreationDate', 'ModDate')}
        document_row.title = pdf_metadata['Title']
        document_row.author = pdf_metadata['Author']

        number_of_pages_threshold = 10
        if pdf_document.number_of_pages > number_of_pages_threshold:
            last_page = number_of_pages_threshold
        else:
            last_page = pdf_document.number_of_pages -1
        self.main_words(pdf_document, last_page)
        
        document_table.add(document_row, commit=False)
        
        return document_row

    ##############################################

    def main_words(self, pdf_document, last_page=None, minimum_count=5, minimum_length=3):

        # Fixme: cache bnc, measure time

        # http://www.lexique.org/listes/liste_mots.php
        
        # ratio unknown > threshold => index error
        # if tag = unknown => language ?

        # language use id
        # indexed word document: id, document, language, word, tag, count, rank
        # indexed word global: id, language, word, tag, count <to learn new word>
 
        # indexer process
        
        words = []
        # Fixme: to iterator ?
        for word_count in pdf_document.collect_document_words(last_page):
            if word_count.count >= minimum_count and len(word_count.word) >= minimum_length:
                word_rows = _bnc_word_table.filter_by(word=word_count.word).all()
                if word_rows:
                    for word_row in word_rows: 
                        if _bnc_database.is_noun(word_row):
                            tag = _bnc_database.part_of_speech_tag_from_id(word_row.part_of_speech_tag_id)
                            print('%6u' % word_count.count, word_count.word, tag)
                            words.append(word_count)
                            break
                else:
                    print('Unknown word %6u' % word_count.count, word_count.word)
                    words.append(word_count)
                
####################################################################################################
# 
# End
# 
####################################################################################################
