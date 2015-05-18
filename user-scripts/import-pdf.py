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

####################################################################################################

from Babel.FileSystem.File import Directory

####################################################################################################

argument_parser = argparse.ArgumentParser()

argument_parser.add_argument('path', metavar='PATH',
                             help='Path')

print('Args:', application.args.user_script_args)
args = argument_parser.parse_args(application.args.user_script_args.split())

####################################################################################################

application.import_path(Directory(args.path))

####################################################################################################
#
# End
#
####################################################################################################
