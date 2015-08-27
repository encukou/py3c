..
    Copyright (c) 2015, Red Hat, Inc. and/or its affiliates
    Copyright (c) 2001-2015 Python Software Foundation; All Rights Reserved
    Licensed under CC-BY-SA-3.0; see the license file

Special Porting Guides
======================

Some porting notes are mentioned outside the main guide, because they
affect fewer project or need more extensive discussion.
Here is a list:

* :doc:`PyCapsule API for Python 2.6 <capsulethunk>`:
    Porting PyCObject while retaining support for Python 2.6

* :doc:`PyFile shim <fileshim>`:
    Quick-and-dirty helpers for porting away from the removed PyFile API

.. toctree::
   :hidden:

   capsulethunk
   fileshim