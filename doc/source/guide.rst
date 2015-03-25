..
    Copyright (c) 2015, Red Hat, Inc. and/or its affiliates
    Licensed under CC-BY-SA-3.0; see the license file


=====================================
Porting guide for Python C Extensions
=====================================

.. highlight:: c

Before you start adding Python 3 compatibility to your C extension,
consider your options:

* .. index:: CFFI
  If you are writing a wrapper for a C library, take a look at
  `CFFI <https://cffi.readthedocs.org>`_, a C Foreign Function Interface
  for Python. This lets you call C from Python 2.6+ and 3.2+, as well as PyPy.
  A C compiler is required for development, but not for installation.

* .. index:: Cython
  For more complex code, consider `Cython <http://cython.org/>`_,
  which compiles a Python-like language to C, has great support for
  interfacing with C libraries, and generates code that works on
  Python 2.6+ and 3.2+.

Using CFFI or Cython will make your code more maintainable in the long run,
at the cost of rewriting the entire extension.
If that's not an option, you will need to update the extension to use
Python 3 APIs. This is where py3c can help.

This is an *opinionated* guide to porting. It does not enumerate your options,
but rather provides one tried way of doing things.

This doesn't mean you can't do things your way – for example, you can
cherry-pick the macros you need and put them directly in your files.
However, dedicated headers for backwards compatibility will make them easier
to find when the time comes to remove them.

If you want more details, consult the
`"Migrating C extensions" chapter <http://python3porting.com/cextensions.html>`_
from Lennart Regebro's book "Porting to Python 3",
the `C porting guide <https://docs.python.org/3/howto/cporting.html>`_
from Python documentation, and the py3c headers for macros to use.


Overview
========

Porting a C extension to Python 3 involves three phases:

1. *Modernization*, where the code is migrated to the latest Python 2 features,
   and tests are added to prevent bugs from creeping in later.
   After this phase, the project will support Python 2.6+.
2. *Porting*, where support for Python 3 is introduced, but Python 2
   compatibility is kept.
   After this phase, the project will support Python 2.6+ and 3.2+.
3. *Cleanup*, where support for Python 2 is removed, and you can start using
   Python 3-only features.
   After this phase, the project will support Python 3.2+.

The first two phases can be done simultaneously; I separate them here because
the porting might require involved discussions/decisions about longer-term
strategy, while modernization can be done immediately
(as soon as support for Python 2.5 is dropped).
But do not let the last two stages overlap,
unless the port is trivial enough to be done in a single patch.
This way you will have working code at all time.

Generally, *libraries*, on which other projects depend, will support
both Python 2 and 3 for a longer time, to allow dependent code to make
the switch. For libraries, the start of phase 3 might be delayed for many years.
On the other hand, *applications* can often switch at once,
dropping Python 2 support as soon as the porting is done.

Let us now look at each step in detail.


.. index::
    single: Modernization

Modernization
=============

Many of Python 3's improvements have been backported to Python 2.6,
so you can start using them immediately.

For all changes you do, be sure add tests to ensure you do not break anything.


.. index::
    double: Modernization; Comparisons

Comparisons
~~~~~~~~~~~

Python 2.1 introduced *rich comparisons* for custom objects, allowing separate
behavior for the ``==``, ``!=``, ``<``, ``>``, ``<=``, ``>=`` operators,
rather than calling one ``__cmp__`` function and interpreting its result
according to the requested operation.
(See `PEP 207 <https://www.python.org/dev/peps/pep-0207/>`_ for details.)

In Python 3, the original ``__cmp__``-based object comparison is removed,
so all code needs to switch to rich comparisons. Instead of a ::

    static int cmp(PyObject *obj1, PyObject *obj2)

function in the ``tp_compare`` slot, there is now a ::

    static PyObject* richcmp(PyObject *obj1, PyObject *obj2, int op)

in the ``tp_richcompare`` slot. The ``op`` argument specifies the comparison
operation: Py_EQ (==), Py_GT (>), Py_LE (<=), etc.

Additionally, Python 3 brings a semantic change. Previously, objects of
disparate types were ordered according to type, where the ordering of types
was undefined (but consistent across, at least, a single invocation of Python).
In Python 3, objects of different types are unorderable.
It is usually possible to write a comparison function that works for both
versions by returning NotImplemented to explicitly fall back to default
behavior.

To help porting from ``__cmp__`` operations, py3c defines a
convenience macro, PY3C_RICHCMP, which evaluates to the right PyObject *
result based on two values orderable by C's comparison operators.
A typical rich comparison function will look something like this::

    static PyObject* mytype_richcmp(PyObject *obj1, PyObject *obj2, int op)
    {
        if (mytype_Check(obj2)) {
            return PY3C_RICHCMP(get_data(obj1), get_data(obj2), op);
        }
        Py_RETURN_NOTIMPLEMENTED;
    }

where ``get_data`` returns an orderable C value (e.g. a pointer or int), and
mytype_Check checks if ``get_data`` is of the correct type
(usually via PyObject_TypeCheck). Note that the first argument, obj1,
is guaranteed to be of the type the function is defined for.

If a "cmp"-style function is provided by the C library,
use ``PY3C_RICHCMP(mytype_cmp(obj1, obj2), 0, op)``.

Also, py3c defines the `Py_RETURN_NOTIMPLEMENTED <https://docs.python.org/3/c-api/object.html#c.Py_RETURN_NOTIMPLEMENTED>`_
macro if it's not provided by your Python version (3.2 and lower).

Note that if you use PY3C_RICHCMP, you will need to include the header
``py3c/comparison.h`` (or copy the macro to your code) even after your port
to Python 3 is complete.
The is also needed for Py_RETURN_NOTIMPLEMENTED until you drop support for
Python 3.2.


.. index::
    double: Modernization; PyObject structure
    double: Modernization; Objects

PyObject Structure Members
~~~~~~~~~~~~~~~~~~~~~~~~~~

To conform to C's strict aliasing rules, PyObject_HEAD, which provides
members such as ``ob_type`` and ``ob_refcnt``, is a separate struct in
Python 3.
Access to these members is provided by macros, which have been ported to
Python 2.6:

==============  ==============
Instead of      use
==============  ==============
obj->ob_type    Py_TYPE(obj)
obj->ob_refcnt  Py_REFCNT(obj)
obj->ob_size    Py_SIZE(obj)
==============  ==============

And for initialization of type objects, the sequence ::

    PyObject_HEAD_INIT(NULL)
    0, /* ob_size */

must be replaced with ::

    PyVarObject_HEAD_INIT(NULL, 0)


.. index::
    double: Modernization; Constants

Adding module-level constants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Often, module initialization uses code like this::

    PyModule_AddObject(m, "RDWR", PyInt_FromLong(O_RDWR));
    PyModule_AddObject(m, "__version__", PyString_FromString("6.28"));

Python 2.6 introduced convenience functions, which are shorter to write::

    PyModule_AddIntConstant(m, "RDWR", O_RDWR)
    PyModule_AddStringConstant(m, "__version__", "6.28")

These will use native int and str types in both Python versions.


.. index::
    double: Modernization; Classes

New-Style Classes
~~~~~~~~~~~~~~~~~

The `old-style classes <https://docs.python.org/2/c-api/class.html>`_
(``PyClass_*`` and ``PyInstance_*``) will be removed in Python 3.
Instead, use `type objects <https://docs.python.org/2/c-api/type.html#typeobjects>`_,
which have been available since Python 2.2.


.. index::
    double: Modernization; PyCObject
    double: Modernization; PyCapsule

PyCObject to PyCapsule
~~~~~~~~~~~~~~~~~~~~~~

The `PyCObject API <https://docs.python.org/3.1/c-api/cobject.html>`_ has been
removed in Python 3.2.
The replacement, `PyCapsule <https://docs.python.org/3/c-api/capsule.html#capsules>`_,
is available in Python 2.7 and 3.1+.

If your project uses PyCObject, and can afford dropping support for Python 2.6,
drop the support and start using PyCapsule instead.


.. index::
    single: Porting

Porting – Adding Support for Python 3
=====================================

The recommended way to port is keeping single-source compatibility between
Python 2 and 3, until support Python 2 can be safely dropped.
For Python code, one can use libraries like `six <https://pypi.python.org/pypi/six/>`_
and `future <http://python-future.org/>`_, and, failing that,
``if sys.version_info >= (3, 0):`` blocks for conditional code.
For C, the py3c library provides common tools, and for special cases you can use
conditional compilation with ``#if IS_PY3``.


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


.. index::
    double: Porting; PyCObject
    double: Porting; PyCapsule

PyCObject to PyCapsule
~~~~~~~~~~~~~~~~~~~~~~

As mentioned in the Modernization section, `PyCObject <https://docs.python.org/3.1/c-api/cobject.html>`_
has been removed in Python 3.2, and the replacement, `PyCapsule <https://docs.python.org/3/c-api/capsule.html#capsules>`_,
is available in Python 2.7 and 3.1+.

Unfortunately, py3c does not yet provide the PyCapsule API for Python 2.6.
Patches are welcome.
Use ``#if IS_PY3`` in the meantime.


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


.. index::
    single: Cleanup

Cleanup – Dropping Support for Python 2
=======================================

When your users are not using Python 2 any more, or you need to use one of
Python 3's irresistible new features, you can convert the project to use
Python 3 only.
As mentioned earlier, it is usually not a good idea to do this until you
have support for both Pythons.

With py3c, this basically amounts to expanding all its compat macros.
Remove the ``py3c.h`` header, and fix the compile errors.

*   .. index::
        double: Cleanup; Strings
        double: Cleanup; Bytes
        double: Cleanup; Unicode

    Convert ``PyStr_*`` to ``PyUnicode_*``; ``PyInt_*`` to ``PyLong_*``.

*   .. index::
        double: Cleanup; Module Initialization

    Instead of ``MODULE_INIT_FUNC(<name>)``, write::

        PyMODINIT_FUNC PyInit_<name>(void);
        PyMODINIT_FUNC PyInit_<name>(void)

*   .. index::
        double: Cleanup; Types

    Remove ``Py_TPFLAGS_HAVE_WEAKREFS`` and ``Py_TPFLAGS_HAVE_ITER``
    (py3c defines them as 0).


*   .. index::
        double: Cleanup; Comparisons

    Replace PY3C_RICHCMP by its expansion, unless you keep the ``py3c/comparison.h``
    header.

*   Replace Py_RETURN_NOTIMPLEMENTED by its expansion, unless you either
    support Python 3.3+ only or keep the ``py3c/comparison.h`` header.

*   Remove any code in ``#if !IS_PY3`` blocks, and the ifs around
    ``#if IS_PY3`` ones.

You will want to check the code as you're doing this.
For example, replacing PyLong can easily result in code like
``if (PyInt_Check(o) || PyInt_Check(o))``.
