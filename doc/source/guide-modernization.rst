..
    Copyright (c) 2015, Red Hat, Inc. and/or its affiliates
    Licensed under CC-BY-SA-3.0; see the license file

.. highlight:: c

.. index::
    single: Modernization

Modernization
=============

Before porting a C extension to Python 3, you'll need to make sure that
you're not using features deprecated even in Python 2.
Also, many of Python 3's improvements have been backported to Python 2.6,
and using them will make the porting process easier.

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

.. note::

    The ``tp_richcompare`` slot is inherited in subclasses together with
    ``tp_hash`` and (in Python 2) ``tp_compare``: iff
    the subclass doesn't define any of them, all are inherited.

    This means that if a class is modernized, its subclasses don't have to be,
    *unless* the subclass manipulates compare/hash slots after
    class creation (e.g. after the :c:func:`PyType_Ready <py3:PyType_Ready>`
    call).


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
You should instead use its replacement, `PyCapsule <https://docs.python.org/3/c-api/capsule.html#capsules>`_.

PyCapsule is available in Python 2.7 and 3.1+.
If you need to support Python 2.6, you can use ``capsulethunk.h``, which
implements the PyCapsule API (with some limitations) in terms of PYCObject.
It is explained in `C Porting HOWTO from the Python documentation
<https://docs.python.org/3/howto/cporting.html#cobject-replaced-with-capsule>`_.

If you use py3c, you can include this header as ``<py3c/capsulethunk.h>``.
It is not included from ``<py3c.h>``, and it comes under a different license.


Done!
~~~~~

When your project is sufficiently modernized, and the tests still pass under
Python 2, you're ready to start the actual :doc:`Porting <guide-porting>`.
