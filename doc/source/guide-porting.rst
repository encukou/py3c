..
    Copyright (c) 2015, Red Hat, Inc. and/or its affiliates
    Licensed under CC-BY-SA-3.0; see the license file

.. highlight:: c

.. index::
    single: Porting

Porting – Adding Support for Python 3
=====================================

After you :doc:`modernize <guide-modernization>` your C extension to use the
latest features available in Python 2, it is time to address the differences
between Python 2 and 3.

The recommended way to port is keeping single-source compatibility between
Python 2 and 3, until support Python 2 can be safely dropped.
For Python code, you can use libraries like `six <https://pypi.python.org/pypi/six/>`_
and `future <http://python-future.org/>`_, and, failing that,
``if sys.version_info >= (3, 0):`` blocks for conditional code.
For C, the py3c library provides common tools, and for special cases you can use
conditional compilation with ``#if IS_PY3``.

To start using py3c, ``#include <py3c.h>``, and instruct your compiler to
find the header.


.. index::
    double: Porting; Strings
    double: Porting; Bytes
    double: Porting; Unicode

The Bytes/Unicode split
~~~~~~~~~~~~~~~~~~~~~~~

The most painful change for extension authors is the bytes/unicode split:
unlike Python 2's ``str`` or C's ``char*``, there is a sharp divide between
*human-readable strings* and *binary data*.
You will need to decide, for each string value you use, which of these two
types you want.

Make the division as sharp as possible: mixing the types tends to lead to utter chaos.
Function that takes both Unicode strings and bytes should be rare,
and should generally be convenience functions in your interface;
not code deep in the internals.

With py3c, the human-readable strings are PyStr_* (PyStr_FromString,
PyStr_Type, PyStr_Check, etc.). They correspond to
`PyString <https://docs.python.org/2/c-api/string.html>`_ on Python 2,
and `PyUnicode <https://docs.python.org/3/c-api/unicode.html>`_ on Python 3.
The supported API is the intersection of `PyString_* <https://docs.python.org/2/c-api/string.html>`_
and `PyUnicode_* <https://docs.python.org/3/c-api/unicode.html>`_,
except PyStr_Size (see below) and the deprecated PyUnicode_Encode;
additionally `PyStr_AsUTF8String <https://docs.python.org/3/c-api/unicode.html#c.PyUnicode_AsUTF8String>`_ is defined.

For binary data, use PyBytes_* (PyBytes_FromString, PyBytes_Type, PyBytes_Check,
etc.). These correspond to PyString on Python 2, and Python 3 provides them
directly.
The supported API is the intersection of `PyString_* <https://docs.python.org/2/c-api/string.html>`_
and `PyBytes_* <https://docs.python.org/3/c-api/bytes.html>`_,

Porting mostly consists of replacing "``PyString_``" to either "``PyStr_``"
or "``PyBytes_``"; just see the caveat about size below.

You might meet two more string types. One is PyUnicode_*, which is provided by
both Python versions directly, and should be used wherever you used PyUnicode
in Python 2 code already.
The other is PyString_*, the Python 2 type used to store both kinds of stringy
data. This type is not in Python 3, and must be replaced.

To summarize:

============ ============= ============== ===================
String kind  py2           py3            Use
============ ============= ============== ===================
PyStr_*      PyString_*    PyUnicode_*    Human-readable text
PyBytes_*    PyString_*    ✔              Binary data
PyUnicode_*  ✔             ✔              Unicode strings
PyString_*   ✔             error          In unported code
============ ============= ============== ===================


.. index::
    double: Porting; String Size

String size
~~~~~~~~~~~

When dealing with Unicode strings, the concept of “size” is tricky,
since the number of characters doesn't necessarily correspond to the
number of bytes in the string's UTF-8 representation.

To prevent subtle errors, this library does *not* provide a
PyStr_Size function.

Instead, use PyStr_AsUTF8AndSize. This functions like Python 3's
`PyUnicode_AsUTF8AndSize <https://docs.python.org/3/c-api/unicode.html#c.PyUnicode_AsUTF8AndSize>`_,
except under Python 2, the string is not encoded (as it should already be in UTF-8),
the size pointer must not be NULL, and the size may be stored even if an error occurs.


.. index::
    double: Porting; Ints
    double: Porting; Long

Ints
~~~~

While string type is split in Python 3, the int is just the opposite:
``int`` and ``long`` were unified. ``PyInt_*`` is gone and only
``PyLong_*`` remains (and, to confuse things further, PyLong is named "int"
in Python code).
The py3c headers alias PyInt to PyLong, so if you're using them,
there's no need to change at this point.


.. index::
    double: Porting; Argument parsing
    double: Porting; PyArg_Parse
    double: Porting; Py_BuildValue

Argument Parsing
~~~~~~~~~~~~~~~~

The format codes for argument-parsing functions of the PyArg_Parse family
have changed somewhat.

In Python 3, the ``s``, ``z``, ``es``, ``es#`` and ``U`` (plus the new ``C``)
codes accept only Unicode strings, while ``c`` and ``S`` only accept bytes.

Formats accepting Unicode strings usually encode to char* using UTF-8.
Specifically, these are ``s``, ``s*``, ``s#``, ``z``, ``z*``, ``z#``, and also
``es``, ``et``, ``es#``, and ``et#`` when the encoding argument is set to NULL.
In Python 2, the default encoding was used instead.

There is no variant of ``z`` for bytes, which means htere's no built-in way to
accept "bytes or NULL" as a ``char*``.
If you need this, write an ``O&`` converter.

Python 2 lacks an ``y`` code, which, in Python 3, works on byte objects.
The use cases needing ``bytes`` in Python 3 and ``str`` in Python 2 should be
rare; if needed, use ``#ifdef IS_PY3`` to select a compatible PyArg_Parse call.

..
    XXX: Write an O& converter for "z" and "y"
    XXX: Write/document handling pathnames safely and portably; see
        PyUnicode_FSConverter/PyUnicode_FSDecoder

Compare the `Python 2 <https://docs.python.org/2/c-api/arg.html>`_ and `Python 3 <https://docs.python.org/3/c-api/arg.html>`_
docs for full details.


.. index::
    double: Porting; Module Initialization


Module initialization
~~~~~~~~~~~~~~~~~~~~~

The module creation process was overhauled in Python 3.
py3c provides a compatibility wrapper so most of the Python 3 syntax can
be used.

PyModuleDef and PyModule_Create
-------------------------------

Module object creation with py3c is the same as in Python 3.

First, create a PyModuleDef structure::

    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        .m_name = "spam",
        .m_doc = PyDoc_STR("Python wrapper for the spam submodule."),
        .m_size = -1,
        .m_methods = spam_methods,
    };

Then, where a Python 2 module would have ::

    m = Py_InitModule3("spam", spam_methods, "Python wrapper ...");

use instead ::

    m = PyModule_Create(&moduledef);

For ``m_size``, use -1. (If you are sure the module supports multiple
subinterpreters, you can use 0, but this is tricky to achieve portably.)
Additional members of the PyModuleDef structure are not accepted under Python 2.

See `Python documentation <https://docs.python.org/3/c-api/module.html#initializing-c-modules_>`_
for details on PyModuleDef and PyModule_Create.

Module creation entrypoint
--------------------------

Instead of the ``void init<name>`` function in Python 2, or a Python3-style
``PyObject *PyInit_<name>`` function, use the MODULE_INIT_FUNC macro
to define an initialization function, and return the created module from it::

    MODULE_INIT_FUNC(name)
    {
        ...
        m = PyModule_Create(&moduledef);
        ...
        if (error) {
            return NULL;
        }
        ...
        return m;
    }


The File API
~~~~~~~~~~~~

The :c:type:`PyFile <py2:PyFileObject>` API was severely reduced
:c:func:`in Python 3 <py3:PyFile_FromFd>`.
The new version is specifically intended for internal error reporting
in Python.

Native Python file objects are officially no longer backed by ``FILE*``.

Use the Python API from the :py:mod:`py3:io` module instead of handling files
in C. The Python API supports all kinds of file-like objects, not just
built-in files – though, admittedly, it's cumbersome to use from plain C.

If you really need to access an API that deals with ``FILE*`` only
(e.g. for debugging), see py3c's limited :doc:`file API shim <fileshim>`.


Other changes
~~~~~~~~~~~~~

If you find a case where py3c doesn't help, use ``#if IS_PY3`` to include
code for only one or the other Python version.
And if your think others might have the same problem,
consider contributing a macro and docs to py3c!


.. index:: Building, ABI tags

Building
~~~~~~~~

When building your extension, note that Python 3.2 introduced ABI version tags
(`PEP 3149 <https://www.python.org/dev/peps/pep-3149/>`_), which can be added
to shared library filenames to ensure that the library is loaded with the
correct Python version. For example, instead of ``foo.so``, the shared library
for the extension module ``foo`` might be named ``foo.cpython-33m.so``.

Your buildsystem might generate these for you already, but if you need to
modify it, you can get the tags from ``systonfig``::

    >>> import sysconfig
    >>> sysconfig.get_config_var('EXT_SUFFIX')
    '.cpython-34m.so'
    >>> sysconfig.get_config_var('SOABI')
    'cpython-34m'

This is completely optional; the old filenames without ABI tags are
still valid.


Done!
~~~~~

Do your tests now pass under both Python 2 and 3?
(And do you have enough tests?)
Then you're done porting!

Once you decide to drop compatibility with Python 2,
you can move to the :doc:`Cleanup <guide-cleanup>` section.
