===============
 PDF Previewer
===============

.. toctree::
  :maxdepth: 2
  :numbered:

Dolphin
=======

Features
--------

* item selection
* drag-and-drop
* divide the space to N columns and an infinite number of rows (vertical slider)
* left click is mapped to open action
* right click is mapped to a contextual menu
* sorting
* splitted-view

Drawbacks
---------

* thumbnails are too small (256 px)
* item selection does not lock files
* file name display is not so useful

Design
======

The PDF previewer aims to show several thumbnails of a the first page of a list of PDF
documents. The thumbnails are placed on a multi-column layout.

Another type of previewer is to display the two first page of a document at once and navigate
through the list using a previous and next action.

Each thumbnail is located in the scene using its grid position. An R-Tree of the bounding boxes
could be used for this purpose. A selection mechanism can be implemented in the corner of the
thumbnail as in Dolphin.

* thumbnail cache
* OpenGL rendering using a texture

.. End
