==========
 PDF Pool
==========

.. toctree::
  :maxdepth: 2
  :numbered:

Requirements
============

Portability Consideration
-------------------------

The portability on NFS is a strong requirement, but it prohibits to use extended file attributes and
inotify API. We can solve this issue using a client-server approach, but it requires to run the
server on the file server.

Types of Hierarchy
==================

Shasum Indexed Hierarchy
------------------------

An sha256 checksum has 256 bit and thus 64 characters in hexadecimal
representation. It provides more than 1e77 keys.

Example::

  8d10b6dd96c1a47aaf41c50f2f7cff6f66f03a58f7ae8587c27d33456a9ede1e

We could create the following hierarchy::

  XX/XX/...

which provides 16**4 = 256 * 256 = 65536 sub-folders.

Topical Hierarchy
-----------------

Example::

  topic1/sub-topic/sub-sub-topic/file.pdf

A journal hierarchy can be included in topical hierarchy.

Author Hierarchy
----------------

Example::

  lastname/firstname/file.pdf

How to connect these hierarchy?
===============================

* using hard-link
 * but it is not portable across file-system, *if we moved the pool then all the inodes will change*
 * hard-links are not preserved by copy
 * rsync requires --hard-links option
 * file is only removed when the counter reaches zero
* using symbolic link
 * Dolphin is able to display preview for them
 * if target is removed then the link is dangling
 * if the link is removed then the target persist
* on Windows / MacOsX ?

File Attributes
===============

For each file we have:

* a pool path
* a path
* a path type: standard file, symbolic link, hard-link
* an inode
* a modification and creation date
* a file size
* a mime-type (from the path, excepted for indexed hierarchy)
* some extended attributes
* a shasum

Inode
-----

A file inode is stable over:

* renaming
* content change
* NFS

An inode is not portable across filesystem.

Python recipe::

  os.stat(file_path).st_ino

Access, Modification and Creation Time
--------------------------------------

Definition:

* atime: time of most recent access,
* mtime: time of most recent content modification,
* ctime: platform dependent
 * time of most recent metadata change on Unix,
 * or the time of creation on Windows

+----------------------------------------------+-----+-----+-----+
| Action                                       |atime|mtime|ctime|
+----------------------------------------------+-----+-----+-----+
|When the file is created                      |  t  |  t  |  t	 |
+----------------------------------------------+-----+-----+-----+
|When the file is modified                     |     |  t  |  t	 |
+----------------------------------------------+-----+-----+-----+
|When the file is renamed                      |     |     |  t	 |
+----------------------------------------------+-----+-----+-----+
|When the file permissions are modified        |     |     |  t	 |
+----------------------------------------------+-----+-----+-----+
|When the file is accessed for the first time  |  t  |	   |	 |
+----------------------------------------------+-----+-----+-----+

A more recent modification time is a signature of a content modification.

Extended User Attributes
------------------------

Extended user attributes are only allowed for regular files and directories.

Is extended file attributes supported by NFSv4?

Man pages:

* attr(5) - extended attributes
* setfattr(1) - set extended attributes of filesystem objects
* getfattr(1) - get extended attributes of filesystem objects
* attr(1) - extended attributes on XFS filesystem objects

Example::

  setfattr -n user.attribute1 -v 1234 a_file
  getfattr -d a_file
    # file: a_file
    user.attribute1="1234"

Python binding: http://pyxattr.k1024.org pyxattr Extended attributes library wrapper for Python

File System Events Monitoring
=============================

Linux provides inotify(7) API.

* OS portability
* Is inotify supported by NFSv4?

References:

* http://inotify.aiken.cz/?section=inotify&page=faq

Python binding: https://github.com/seb-m/pyinotify

pyinotify test::

  python -m pyinotify -v /tmp

External Modification
=====================

For indexed hierarchy, we prohibit external modification.

For other hierarchy, a file can be:

* moved within the pool
* renamed (similar to moved)
* deleted (or moved outside the pool)
* modified

How to detect these cases?:

* moved/renamed = same inode/shasum and different path
* deleted = any file having this inode/shasum
* modified = same inode/path and more recent mtime and shasum different

How to Check the Pool Coherency?
================================

Shasum Indexed Hierarchy
------------------------

We assume there is any external modification to the file hierarchy.

For shasum indexed hierarchy, the shasum path identify uniquely the file.

Check Algorithm::

  for file in pool:
    if file shasum not in database:
       file is new

  for file in database:
    if file path doesn't exists:
       file was removed

A content update will change the shasum and thus imply a missing and new file.

other Hierarchies
-----------------

For other hierarchies, we cannot use the path as a key since the file name could be renamed. We can
use instead the inode or an unique identifier extended attribute.

.. The inode is conserved for file copy. = modification

Design Cases
============

Case 1
------

Design:

* file are stored in an indexed hierarchy
* symbolic link are used for topical hierarchy

Properties:

* the pool cannot have doublon
* symbolic link targets the shasum
* to delete a file we have to delete it from the indexed hierarchy

Case 2
------

Design:

* the pool uses hard link to connect the hierarchies
* the pool uses an indexed hierarchy

Properties:

* the pool cannot have doublon
* we don't have a direct path from link to the indexed hierarchy
* to delete a file we have to delete it from the indexed hierarchy
* we have to use rsync to copy the pool

How to Synchronise two Pools?
=============================

.. End
