####################################################################################################
# 
# Babel - 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

class Walk(object):

    ##############################################

    def __walk__(path, followlinks=False):

        for root, dirs, files in os.walk(path):
            for filename in files:

####################################################################################################
# 
# End
# 
####################################################################################################
