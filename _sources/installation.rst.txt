.. include:: project-links.txt
.. include:: abbreviation.txt

.. _installation-page:

==============
 Installation
==============

On Windows
----------

Firstly, you have to install the `Anaconda Distribution <https://www.anaconda.com/download/>`_ so
as to get a full featured Python 3 environment.

Then open the `Anaconda Navigator <https://docs.continuum.io/anaconda/navigator/>`_ and launch a console for your root environment.

You can now run *pip* to install Babel in your root environment using this command:

.. code-block:: sh

  pip install Babel

On Linux
--------

Firstly, you have to install Python 3 from your distribution.

Then you can install Babel using *pip* or from source. See supra.

On OSX
------

There are several ways to get Python on OSX:

 * use the built in Python
 * install `Miniconda <https://conda.io/miniconda.html>`_
 * install the `Anaconda Distribution <https://www.anaconda.com/download/>`_.
 * install from Brew `brew install python3` **(reported to work)**

You can install Babel using *pip* or from source. See supra.

Installation from PyPi Repository
---------------------------------

Babel is available on the Python Packages |Pypi|_ repository at |Babel@pypi|

Run this command in the console to install the latest release:

.. code-block:: sh

  pip install Babel

Install a more recent version from Github
-----------------------------------------

If you want to install a version which is not yet released on Pypi, you can use one of theses
commands to install the stable or devel branch:

.. code-block:: sh

  pip install git+https://github.com/FabriceSalvaire/Babel

  pip install git+https://github.com/FabriceSalvaire/Babel@devel

Installation from Source
------------------------

The Babel source code is hosted at |Babel@github|

.. add link to pages ...

You have to solution to get the source code, the first one is to clone the repository, but if you
are not familiar with Git then you can simply download an archive either from the Babel Pypi page
(at the bottom) or the GitHub page (see clone or download button).

To clone the Git repository, run this command in a console:

.. code-block:: sh

  git clone https://github.com/FabriceSalvaire/Babel.git

Then to build and install Babel run these commands:

.. code-block:: sh

  python setup.py build
  python setup.py install

Dependencies
------------

Babel requires the following dependencies:

 * |Python|_ 3
 * PyQt5
