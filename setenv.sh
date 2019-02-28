# append_to_path_if_not ${PWD}/bin
# append_to_path_if_not ${PWD}/tools

# append_to_ld_library_path_if_not /usr/local/stow/mupdf-1.12/lib/
# export MUPDF_LIBRARY=/usr/local/stow/mupdf-1.12/lib/libmupdf.so
export MUPDF_LIBRARY_PATH=/usr/local/stow/mupdf-1.12/lib

/bin/rm -f _mupdf.cpython-36m-x86_64-linux-gnu.so
ln -sf build/lib.linux-x86_64-3.6/_mupdf.cpython-36m-x86_64-linux-gnu.so

source /opt/python-virtual-env/py37/bin/activate

append_to_python_path_if_not ${PWD}
append_to_python_path_if_not ${PWD}/external-packages/
