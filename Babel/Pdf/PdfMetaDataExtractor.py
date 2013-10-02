####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################
# 
#                                              audit 
# 
# - 12/08/2013 Fabrice
# 
####################################################################################################

####################################################################################################

from .PdfDocument import PdfDocument
from .TextTokenizer import strip_word_list
from Babel.Tools.DictionaryTools import DictInitialised
from Babel.Tools.Statistics import Gaussian

####################################################################################################

class PdfMetaDataExtractor(object):

    """ This class implements a PDF document Metadata Extractor. """

    address_words = set((
            'avenue',
            'france',
            'institute',
            'rue',
            'university',
            'usa',
            ))

    ##############################################

    def __init__(self, path):

        self._pdf_document = PdfDocument(path)

        self._document_metadata = DocumentMetaData()

        self._document_metadata['number_of_pages'] = self._pdf_document.number_of_pages

        # metadata = pdf_document.metadata
        # for key in sorted(metadata.iterkeys()):
        #     unicode(metadata[key])

        self._first_text_page = self._pdf_document.first_page.text
        self._first_text_blocks = self._first_text_page.blocks

        self._guess_title()
        self._guess_authors()

    ##############################################

    @property
    def title(self):
        return unicode(self._title_block)

    ##############################################

    @property
    def authors(self):
        return self._authors

    ##############################################

    @property
    def number_of_pages(self):
        return self._document_metadata['number_of_pages']

    ##############################################

    @property
    def metadata(self):
        return self._pdf_document.metadata

    ##############################################

    def _first_text_blocks_iterator(self):

        return self._first_text_blocks.sorted_iter()

    ##############################################

    def dump(self):

        print 'Number of pages:', self._pdf_document.number_of_pages
        metadata = self._pdf_document.metadata
        for key in sorted(metadata.iterkeys()):
            print key + ': ' + unicode(metadata[key])
        
        for text_block in self._first_text_blocks_iterator(): 
        
            template = """
        Block %u
          y rank %u
          Interval %s
          Horizontal Margin %s
          Is centred %s
          Is left justifier %g
          Is right justifier %g
          Number of characters %u
          Number of words %u
          main style %s
        """
            print template[:-1] % (text_block.block_id,
                                   text_block.y_rank,
                                   text_block.interval,
                                   str(text_block.horizontal_margin),
                                   text_block.is_centred,
                                   text_block.is_left_justified,
                                   text_block.is_right_justified,
                                   len(text_block),
                                   text_block.tokenised_text.count_word_number(),
                                   str(text_block.main_style)
                                   )
            line = '='*100
            print line
            print unicode(text_block)
            print line

    ##############################################

    def _guess_title(self):

        # Fixme: inference ?

        probabilities = TextBlockProbabilities()
        for text_block in self._first_text_blocks_iterator():
            title_gaussian_style_rank = Gaussian(0, 1)
            title_gaussian_y_rank = Gaussian(0, 3)
            p0 = title_gaussian_style_rank(text_block.main_style.rank)
            p1 = title_gaussian_y_rank(text_block.y_rank)
            probability = p0*p1
            # print 'Title probability', probability
            probabilities.add_candidate(text_block=text_block, probability=probability)
        probabilities.sort()

        text_block_probability = probabilities.most_probable()
        self._title_block = text_block_probability.text_block

    ##############################################

    def _guess_authors(self):

        probabilities = TextBlockProbabilities()
        for text_block in self._first_text_blocks.sorted_iter():
            author_gaussian_y_rank = Gaussian(self._title_block.y_rank +1, 1)
            author_gaussian_number_of_words = Gaussian(10, 5)
            number_of_words = text_block.tokenised_text.count_word_number()
            p0 = author_gaussian_y_rank(text_block.y_rank)
            p1 = author_gaussian_number_of_words(number_of_words)
            probability = p0*p1
            # print 'Author probability', probability
            probabilities.add_candidate(text_block=text_block, probability=probability)
        probabilities.sort()

        author_block = None
        for text_block_probability in probabilities:
            text_block = text_block_probability.text_block
            if text_block is not self._title_block:
                author_block = text_block
                break
        else:
            author_block = None

        self._author_block = author_block

        author_list_words = []
        for i, line in enumerate(author_block.line_iterator()):
            line_words = []
            for word in line.tokenised_text:
                if word.is_word and unicode(word).lower() in self.address_words:
                    break
                else:
                    line_words.append(word)
            else:
                author_list_words += line_words

        author_separators = []
        for i, word in enumerate(author_list_words):
            if word.is_word and unicode(word).lower() == 'and': 
                author_separators.append(i)
        lower_index = 0
        number_of_words = len(author_list_words)
        if author_separators[-1] != number_of_words -1:
           author_separators.append(number_of_words) 
        self._authors = []
        for upper_index in author_separators:
            author_words = author_list_words[lower_index:upper_index]
            author_words = strip_word_list(author_words)
            self._authors.append(author_words)
            lower_index = upper_index +1

####################################################################################################

class TextBlockProbability(DictInitialised):

    """
    
    Public Attributes:

      :attr:`text_block`

      :attr:`probability`

    """

    __REQUIRED_ATTRIBUTES__ = (
        'text_block',
        'probability',
        )

    ##############################################

    def __cmp__(self, other):

        return cmp(self.probability, other.probability)

####################################################################################################

class TextBlockProbabilities(list):

    ##############################################

    def add_candidate(self, **kwargs):

        text_block_probability = TextBlockProbability(**kwargs)
        self.append(text_block_probability)

    ##############################################

    def sort(self):

        super(TextBlockProbabilities, self).sort(reverse=True)

    ##############################################

    def most_probable(self):

        return self[0]

####################################################################################################

class DocumentMetaData(dict):
    pass

####################################################################################################
# 
# End
# 
####################################################################################################
