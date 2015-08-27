..
    Copyright (c) 2015, Red Hat, Inc. and/or its affiliates
    Copyright (c) 2001-2015 Python Software Foundation; All Rights Reserved
    Licensed under CC-BY-SA-3.0; see the license file

PyCapsule API for Python 2.6
============================

The ``capsulethunk.h`` heared, implements the PyCapsule API
(with some limitations) in terms of PYCObject.
It is only necessary for compatibility with Python 2.6 (or 3.0).

.. note::
    The ``capsulethunk.h`` header and this documentation was written by
    Larry Hastings for the Python documentation.
    It is now maintained as part of the py3c project.

CObject replaced with Capsule
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :c:type:`Capsule` object was introduced in Python 3.1 and 2.7 to replace
:c:type:`CObject`.  CObjects were useful,
but the :c:type:`CObject` API was problematic: it didn't permit distinguishing
between valid CObjects, which allowed mismatched CObjects to crash the
interpreter, and some of its APIs relied on undefined behavior in C.
(For further reading on the rationale behind Capsules, please see :issue:`5630`.)

If you're currently using CObjects, and you want to migrate to 3.1 or newer,
you'll need to switch to Capsules.
:c:type:`CObject` was deprecated in 3.1 and 2.7 and completely removed in
Python 3.2.  If you only support 2.7, or 3.1 and above, you
can simply switch to :c:type:`Capsule`.  If you need to support Python 3.0,
or versions of Python earlier than 2.7,
you'll have to support both CObjects and Capsules.
(Note that Python 3.0 is no longer supported, and it is not recommended
for production use.)

The following example header file :file:`capsulethunk.h` may
solve the problem for you.  Simply write your code against the
:c:type:`Capsule` API and include this header file after
:file:`Python.h`.  Your code will automatically use Capsules
in versions of Python with Capsules, and switch to CObjects
when Capsules are unavailable.

:file:`capsulethunk.h` simulates Capsules using CObjects.  However,
:c:type:`CObject` provides no place to store the capsule's "name".  As a
result the simulated :c:type:`Capsule` objects created by :file:`capsulethunk.h`
behave slightly differently from real Capsules.  Specifically:

  * The name parameter passed in to :c:func:`PyCapsule_New` is ignored.

  * The name parameter passed in to :c:func:`PyCapsule_IsValid` and
    :c:func:`PyCapsule_GetPointer` is ignored, and no error checking
    of the name is performed.

  * :c:func:`PyCapsule_GetName` always returns NULL.

  * :c:func:`PyCapsule_SetName` always raises an exception and
    returns failure.  (Since there's no way to store a name
    in a CObject, noisy failure of :c:func:`PyCapsule_SetName`
    was deemed preferable to silent failure here.  If this is
    inconvenient, feel free to modify your local
    copy as you see fit.)

You can find :file:`capsulethunk.h` in the Python source distribution
as :source:`include/py3c/capsulethunk.h`.  We also include it here for
your convenience:

.. literalinclude:: ../../include/py3c/capsulethunk.h
