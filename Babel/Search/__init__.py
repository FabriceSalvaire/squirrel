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

from ..Logging.LogPrinting import format_frame

####################################################################################################

class Searcher:

    ##############################################

    def __init__(self, application):

        self._application = application

        self._whoosh_database = application.whoosh_database

        self._document_database = application.document_database
        self._document_table = self._document_database.document_table
        self._word_table = self._document_database.word_table

    ##############################################

    def search_in_whoosh(self, query):

        hits = self._whoosh_database.search(query)

        for hit in hits:
            shasum = hit['shasum']
            rows = self._document_table.filter_by(shasum=shasum)
            for document_row in rows:
                yield document_row

    ##############################################

    def search_in_word_table(self, query):

        words = [word.lower() for word in query.split() if word]

        # rows = None
        # for word in words:
        #     print('word:', word)
        #     if rows is None:
        #         rows = self._word_table
        #     rows = rows.filter_by(word=word)

        rows = self._word_table.filter_by(word=words[0])

        # Fixme: should be one
        for word_row in rows:
            for document_row in  word_row.documents:
                yield document_row

    ##############################################

    def _print_document(self, document):

            message = """
Title    {0.title}

Path     {0.path.directory}
         {0.path.filename}
Shasum   {0.shasum}
Author   {0.author}
Page     {0.number_of_pages}
Language {0.language}
Comment  {0.comment}
""".strip()

            text = message.format(document)
            print(format_frame(text, margin=True))

    ##############################################

    def console_search(self, args):

        query = args.query

        text = 'Query: {}'.format(query)
        print(format_frame(text, margin=True))

        # for document in self.search_in_whoosh(query):
        #     self._print_document(document)

        for document in self.search_in_word_table(query):
            self._print_document(document)
