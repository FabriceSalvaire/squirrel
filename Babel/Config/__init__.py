####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

import os

####################################################################################################

def create_user_directories(path_config):

    for purpose, directory in (
        ('config', path_config.config_directory),
        ('data', path_config.data_directory),
        ):
        create_user_directory(purpose, directory)

####################################################################################################

def create_user_directory(purpose, directory):

    if not os.path.isabs(directory):
        raise ValueError("%s directory must be absolut (given is %s)" %
                         (purpose.title(), directory))
    if not os.path.exists(directory):
        os.mkdir(directory)
    elif not os.path.isdir(directory):
        raise ValueError("Path for %s directory is not a directory (given is %s)" %
                         (purpose, directory))

####################################################################################################
# 
# End
# 
####################################################################################################
