.. -*- Mode: rst -*-

.. -*- Mode: rst -*-

..
   |BabelUrl|
   |BabelHomePage|_
   |BabelDoc|_
   |Babel@github|_
   |Babel@readthedocs|_
   |Babel@readthedocs-badge|
   |Babel@pypi|_

.. |ohloh| image:: https://www.openhub.net/accounts/230426/widgets/account_tiny.gif
   :target: https://www.openhub.net/accounts/fabricesalvaire
   :alt: Fabrice Salvaire's Ohloh profile
   :height: 15px
   :width:  80px

.. |BabelUrl| replace:: https://fabricesalvaire.github.io/Biblio

.. |BabelHomePage| replace:: Babel Home Page
.. _BabelHomePage: https://fabricesalvaire.github.io/Biblio

.. |Babel@readthedocs-badge| image:: https://readthedocs.org/projects/Babel/badge/?version=latest
   :target: http://Babel.readthedocs.org/en/latest

.. |Babel@github| replace:: https://github.com/FabriceSalvaire/Babel
.. .. _Babel@github: https://github.com/FabriceSalvaire/Babel

.. |Babel@pypi| replace:: https://pypi.python.org/pypi/Babel
.. .. _Babel@pypi: https://pypi.python.org/pypi/Babel

.. |Build Status| image:: https://travis-ci.org/FabriceSalvaire/Babel.svg?branch=master
   :target: https://travis-ci.org/FabriceSalvaire/Babel
   :alt: Babel build status @travis-ci.org

.. |Pypi Version| image:: https://img.shields.io/pypi/v/Babel.svg
   :target: https://pypi.python.org/pypi/Babel
   :alt: Babel last version

.. |Pypi License| image:: https://img.shields.io/pypi/l/Babel.svg
   :target: https://pypi.python.org/pypi/Babel
   :alt: Babel license

.. |Pypi Python Version| image:: https://img.shields.io/pypi/pyversions/Babel.svg
   :target: https://pypi.python.org/pypi/Babel
   :alt: Babel python version

..  coverage test
..  https://img.shields.io/pypi/status/Django.svg
..  https://img.shields.io/github/stars/badges/shields.svg?style=social&label=Star
.. -*- Mode: rst -*-

.. |Python| replace:: Python
.. _Python: http://python.org

.. |PyPI| replace:: PyPI
.. _PyPI: https://pypi.python.org/pypi

.. |Numpy| replace:: Numpy
.. _Numpy: http://www.numpy.org

.. |IPython| replace:: IPython
.. _IPython: http://ipython.org

.. |Sphinx| replace:: Sphinx
.. _Sphinx: http://sphinx-doc.org

.. End

=======
 Babel
=======

|Pypi License|
|Pypi Python Version|

|Pypi Version|

* Quick Link to `Production Branch <https://github.com/FabriceSalvaire/Babel/tree/master>`_
* Quick Link to `Devel Branch <https://github.com/FabriceSalvaire/Babel/tree/devel>`_

Overview
========

.. image:: https://raw.github.com/FabriceSalvaire/Biblio/master/doc/sphinx/source/_static/pdf-browser.pdf-viewer-mode.png
.. image:: https://raw.github.com/FabriceSalvaire/Biblio/master/doc/sphinx/source/_static/pdf-browser.browser-mode.png

What is Babel ?
---------------

Babel was an attempt to develop a PDF document manager.

Actually it features:

* a PDF browser that permit to navigate in the file system, display PDF documents and sort (move)
  them in a similar way than the Geeqie image viewer.
* a GUI showing the PDF document metadatas, pages and corresponding text blocks.
* tools to generate thumbnails, extract text from pages
* a `MuPDF <https://mupdf.com>`_ binding using `CFFI <https://cffi.readthedocs.io/en/latest>`_ ( **it need a dynamic library and API update** )

  see also https://github.com/FabriceSalvaire/mupdf-cmake

* a BibTeX parser
* Lexique tool using British National Corpus
* *some experimental codes to extract metadata, text, and index them.*

  To go further, look at https://whoosh.readthedocs.io and https://www.elastic.co/products/elasticsearch

Where is the Documentation ?
----------------------------

The documentation is available on the |BabelHomePage|_.

How to install it ?
-------------------

Look at the `installation <https://fabricesalvaire.github.io/Biblio/installation.html>`_ section in the documentation.

Credits
=======

Authors: `Fabrice Salvaire <http://fabrice-salvaire.fr>`_

News
====

.. -*- Mode: rst -*-


.. no title here

V0 2013-02-11 
-------------

Started project

.. End
