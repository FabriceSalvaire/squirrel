####################################################################################################

append_to_path_if_not ${PWD}/bin
append_to_path_if_not ${PWD}/tools

append_to_ld_library_path_if_not /usr/local/stow/mupdf/lib/
export MUPDF_LIBRARY=/usr/local/stow/mupdf/lib/libmupdf-js-v8.so
export LD_LIBRARY_PATH

source /opt/python-virtual-env/py35/bin/activate

append_to_python_path_if_not ${PWD}

####################################################################################################
#
# End
#
####################################################################################################
