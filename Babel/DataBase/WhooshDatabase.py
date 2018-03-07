####################################################################################################
#
# Babel - A Bibliography Manager
# Copyright (C) 2017 Fabrice Salvaire
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

import os

from whoosh.analysis import (
    RegexTokenizer,
    StandardAnalyzer, StemmingAnalyzer,
    LowercaseFilter, StemFilter, StopFilter # , CharsetFilter
)
from whoosh.fields import *
from whoosh.qparser import QueryParser
import whoosh

####################################################################################################

class WhooshDatabase:

    ##############################################

    def __init__(self, path):

        # tokenizer = RegexTokenizer()
        # lower_case_filter = LowercaseFilter()
        # stem_filter = StemFilter()
        # stop_filter = StopFilter()
        # analyser = tokenizer | lower_case_filter | stop_filter | stem_filter

        # combines a tokenizer, lower-case filter, optional stop filter, and stem filter
        self._analyser = StemmingAnalyzer(
            minsize=2, # Words smaller than this are removed from the stream
            maxsize=30,
            cachesize=-1, # Set the cachesize to -1 to indicate unbounded caching
        )

        self._schema = Schema(shasum=ID(stored=True), content=TEXT(analyzer=self._analyser))

        if not os.path.exists(path):
            os.mkdir(path)
            self._index = whoosh.index.create_in(path, self._schema)
        else:
            self._index = whoosh.index.open_dir(path)

    ##############################################

    def _new_writer(self):

        return self._index.writer(
            limitmb=512, # maximum memory (in megabytes) the writer will use for the indexing pool
            procs=4, # number of processors the writer will use for indexing
            # multisegment=True,
        )

    ##############################################

    def __del__(self):

        self._writer.commit()

    ##############################################

    def index(self, shasum, content):

        with self._new_writer() as writer:
            writer.add_document(shasum=shasum, content=content)

    ##############################################

    def search(self, query_str):

        results = None
        with self._index.searcher() as searcher:
            # results = searcher.lexicon("content")
            # for result in results:
            #     print(result.decode('utf-8'))
            query = QueryParser('content', self._index.schema).parse(query_str)
            results = searcher.search(query)
            for result in results:
                yield result

