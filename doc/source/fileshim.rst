..
    Copyright (c) 2015, Red Hat, Inc. and/or its affiliates
    Copyright (c) 2001-2015 Python Software Foundation; All Rights Reserved
    Licensed under CC-BY-SA-3.0; see the license file

.. highlight:: c

.. index::
    double: Porting; PyFile

The PyFile API
==============

In Python 3, the PyFile API was reduced to a few functions, and is now
meant for internal interpreter use.

Python files (and file-like objects) should be manipulated with the API defined
by the :py:mod:`py3:io` module.


But, in the real world, some C libraries only provide debugging output to
``FILE*``. For cases like this, py3c provides a quick-and-dirty replacement
for :c:func:`py2:PyFile_AsFile`: ``py3c_PyFile_AsFileWithMode`` which takes
a ``PyObject *`` (which must be a file with a working ``fileno()`` method) and
a ``const char *mode``, which must be an appropriate mode argument for
``fdopen``, and returns a ``FILE*``.

This function presents several caveats:

* Only works on file-like objects backed by an actual file
* All C-level writes should be done before additional
  Python-level writes are allowed (e.g. by running Python code).
* Though the function tries to flush, there is no guarantee that
  writes will be reordered due to different layers of buffering.
