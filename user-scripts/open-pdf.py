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

import argparse
import os

####################################################################################################

from Babel.FileSystem.File import File, Path

####################################################################################################

argument_parser = argparse.ArgumentParser()

argument_parser.add_argument('filename', metavar='FILE',
                             help='PDF file')

print('Args:', application.args.user_script_args)
args = argument_parser.parse_args(application.args.user_script_args.split())

####################################################################################################

file_path = File(os.path.expanduser(args.filename)) # Fixme:
application.open_pdf(file_path)

####################################################################################################
#
# End
#
####################################################################################################
