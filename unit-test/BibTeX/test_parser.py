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
