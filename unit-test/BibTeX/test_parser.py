####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

import logging
logging.basicConfig(format='\033[1;34m%(name)s - %(module)s.%(funcName)s\033[0m - %(message)s',
#                   level=logging.DEBUG,
                    level=logging.INFO,
                    )

####################################################################################################

from BibTeX.Parser import Parser

####################################################################################################

with open('test1.bib', 'r') as f:
    data = f.read()

parser = Parser()
#parser.test_lexer(data)
entries = parser.parse(data)
for entry in entries:
    print(entry)

####################################################################################################
# 
# End
# 
####################################################################################################
