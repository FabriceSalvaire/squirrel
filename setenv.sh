####################################################################################################

append_to_path_if_not ${PWD}/bin
append_to_path_if_not ${PWD}/tools

append_to_ld_library_path_if_not /usr/local/stow/openjpeg2/lib/
append_to_ld_library_path_if_not /usr/local/stow/mupdf-1.3/lib/

source /srv/scratch/python-virtual-env/standard/bin/activate
append_to_python_path_if_not ${PWD}
append_to_python_path_if_not /usr/local/stow/mupdf-1.3/lib/python/

####################################################################################################
# 
# End
# 
####################################################################################################
