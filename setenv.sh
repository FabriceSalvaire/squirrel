append_to_path_if_not ${PWD}/bin
append_to_path_if_not ${PWD}/tools

# append_to_ld_library_path_if_not /usr/local/stow/mupdf/lib/
# export MUPDF_LIBRARY=/usr/local/stow/mupdf/lib/libmupdf-js-v8.so

append_to_ld_library_path_if_not /usr/local/stow/mupdf-1.11/lib/
export MUPDF_LIBRARY=/usr/local/stow/mupdf-1.11/lib/libmupdf.so

rm _mupdf.cpython-36m-x86_64-linux-gnu.so
ln -sf build/lib.linux-x86_64-3.6/_mupdf.cpython-36m-x86_64-linux-gnu.so

source /opt/python-virtual-env/py36/bin/activate

append_to_python_path_if_not ${PWD}
