####################################################################################################

append_to_path_if_not ${PWD}/bin
append_to_path_if_not ${PWD}/tools

append_to_ld_library_path_if_not ${PWD}/../mupdf-fabrice-build

append_to_python_path_if_not ${PWD}
append_to_python_path_if_not ${PWD}/../mupdf-fabrice/bindings/
append_to_python_path_if_not ${PWD}/../mupdf-fabrice-build/bindings/

####################################################################################################
# 
# End
# 
####################################################################################################
