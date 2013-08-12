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

####################################################################################################

from Babel.Pdf.PdfDocument import PdfDocument
from Babel.Pdf.TextTokenizer import TextTokenizer
from Babel.Tools.DictionaryTools import DictInitialised
from Babel.Tools.ProgramOptions import PathAction
from Babel.Tools.Statistics import Gaussian

####################################################################################################

class PdfMetaDataExtractor(object):

    """ This class implements a PDF document Metadata Extractor. """

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

        title_probabilities = TextBlockProbabilities()
        for text_block in self._first_text_blocks_iterator():
            title_gaussian_style_rank = Gaussian(0, 1)
            title_gaussian_y_rank = Gaussian(0, 3)
            p0 = title_gaussian_style_rank(text_block.main_style.rank)
            p1 = title_gaussian_y_rank(text_block.y_rank)
            title_probability = p0*p1
            print 'Title probability', title_probability
            text_block_probability = TextBlockProbability(text_block=text_block, probability=title_probability)
            title_probabilities.append(text_block_probability)
        title_probabilities.sort()
        text_block_probability = title_probabilities.most_probable()
        self._title_block = text_block_probability.text_block

    ##############################################

    def _guess_author(self):

        author_probabilities = TextBlockProbabilities()
        for text_block in self._first_text_blocks.sorted_iter():
            author_gaussian_y_rank = Gaussian(self._title_block.y_rank +1, 1)
            author_gaussian_number_of_words = Gaussian(10, 5)
            number_of_words = text_block.tokenised_text.count_word_number()
            p0 = author_gaussian_y_rank(text_block.y_rank)
            p1 = author_gaussian_number_of_words(number_of_words)
            author_probability = p0*p1
            print 'Author probability', author_probability
            text_block_probability = TextBlockProbability(text_block=text_block, probability=author_probability)
            author_probabilities.append(text_block_probability)
        author_probabilities.sort()
        author_block = None

        i = 0
        while i < len(author_probabilities):
            d = author_probabilities[i]
            block = d.text_block
            if block is not self._title_block:
                author_block = block
                break
            else:
                i += 1

        self._author_block = author_block

        print unicode(author_block)
        for line in author_block.line_iterator():
            for span in line:
                print span

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
