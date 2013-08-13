####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

import argparse

####################################################################################################

from Babel.FileSystem.File import File

####################################################################################################

argument_parser = argparse.ArgumentParser()

argument_parser.add_argument('filename', metavar='FILE',
                             help='PDF file')

print 'Args:', application.args.user_script_args
args = argument_parser.parse_args(application.args.user_script_args.split())

####################################################################################################

application.open_pdf(File(args.filename))

####################################################################################################
#
# End
#
####################################################################################################