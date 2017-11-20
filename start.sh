####################################################################################################
#
# How to Start
#
####################################################################################################

# Set the environment
. setenv.sh

# PyQt
./tools/make-gui

# Build
python setup.py build

# Generate RST files
##./tools/generate-rst
# Generate HTML Documentation
# cd sphinx/
##./make-html --clean
