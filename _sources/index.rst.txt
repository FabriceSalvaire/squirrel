.. include:: abbreviation.txt
.. include:: project-links.txt

.. raw:: html

    <style>
        .small-text {font-size: smaller}

	.spacer {height: 30px}

        .reduced-width {
	    max-width: 800px
        }

        .row {clear: both}

        @media only screen and (min-width: 1000px),
               only screen and (min-width: 500px) and (max-width: 768px){

            .column {
                padding-left: 5px;
                padding-right: 5px;
                float: left;
            }

            .column2  {
                width: 50%;
            }

            .column3  {
                width: 33.3%;
            }
        }
    </style>

.. raw:: html

   <div class="reduced-width">

########
 Title
########

.. .. image:: /_static/logo.png
       :alt: Babel logo
       :width: 750

********
Overview
********

Babel is a free and open source (*) Python module which interface |Python|_ ...

.. rst-class:: small-text

    (*) Babel is licensed under GPLv3 therms.

Babel requires Python 3 and works on Linux, Windows and OS X.

:ref:`To read more on Babel <overview-page>`

.. raw:: html

   <div class="spacer"></div>

.. rst-class:: clearfix row

.. rst-class:: column column2

:ref:`news-page`
================

What's changed in versions

.. rst-class:: column column2

:ref:`Installation-page`
========================

How to install Babel on your system

.. rst-class:: column column2

:ref:`user-faq-page`
====================

Answers to frequent questions

.. rst-class:: column column2

:ref:`development-page`
=======================

How to contribute to the project

.. rst-class:: column column2

:ref:`reference-manual-page`
============================

Technical reference material, for classes, methods, APIs, commands.

.. rst-class:: column column2

:ref:`how-to-refer-page`
========================

Guidelines to cite Babel

.. raw:: html

   </div>

.. why here ???

.. rst-class:: clearfix row

.. raw:: html

   <div class="spacer"></div>

*******************
 Table of Contents
*******************

.. toctree::
  :maxdepth: 3
  :numbered:

  overview.rst
  news.rst
  roadmap.rst
  installation.rst
  faq.rst
  design-notes/index.rst
  reference-manual.rst
  development.rst
  how-to-refer.rst
  related-projects.rst
  bibliography.rst

..

  donate.rst
