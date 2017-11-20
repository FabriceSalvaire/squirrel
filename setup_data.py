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

import os

####################################################################################################

# Utility function to read the README file.
# Used for the long_description.
def read(file_name):

    path = os.path.dirname(__file__)
    if os.path.basename(path) == 'tools':
        path = os.path.dirname(path)
    absolut_file_name = os.path.join(path, file_name)

    return open(absolut_file_name).read()

####################################################################################################

from BabelBuild.MuPdf import build_mupdf

setup_dict = dict(
    name='babel',
    version='0.1.0',
    author='Fabrice Salvaire',
    author_email='fabrice.salvaire@orange.fr',
    description='A Bibliography Manager',
    license = "GPLv3",
    keywords = "bibliography",
    url='http://fabrice-salvaire.pagesperso-orange.fr/software/index.html',
    long_description=read('README.txt'),
    # cf. http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Education",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        ],
    # install_requires=[
    #     "cffi>=1.0.0"
    #     # 'pyqt>=4.9',
    #     ],
    ext_modules=[build_mupdf.ffi.distutils_extension()],
    # setup_requires=["cffi>=1.0.0"],
    # cffi_modules=['Babel/MuPdf/build_mupdf.py:ffi'],
    scripts=['bin/babel'],
    packages=['Babel'],
    data_files = [('share/Babel/icons',['share/icons/babel.svg']),
                  ('share/applications', ['spec/babel.desktop']),
    ],
)
