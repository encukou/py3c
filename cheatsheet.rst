~~~~~~~~~~~~~~~
py3c cheatsheet
~~~~~~~~~~~~~~~

Use
===

Strings
~~~~~~~

* PyStr_* – for human-readable strings

* PyBytes_* – for binary data

* PyUnicode_* – when you used ``unicode`` in Python 2

* PyString_* – when you don't care about Python 3

Ints
~~~~

Use whatever you used in Python 2. For py3-only code, use PyLong.

Comparison
~~~~~~~~~~

Use rich comparison.
A convenience macro, PY_RICHCMP(a, b, op), is provided to help common cases.

Objects
~~~~~~~

Use ``Py_TYPE(obj)`` instead of ``obj->ob_type``.

Use ``PyVarObject_HEAD_INIT(NULL, 0)`` instead of ``PyObject_HEAD_INIT(NULL), 0``.

Module initialization
~~~~~~~~~~~~~~~~~~~~~

Write things as in Python 3, but:

    * MODULE_INIT_FUNC to declare+define the init function.
    * Do not use ``m_reload``, ``m_traverse``, ``m_clear``, ``m_free`` in moduledef

The code will look like this::

    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        .m_name = "spam",
        .m_doc = PyDoc_STR("Python wrapper for the spam submodule."),
        .m_size = -1,
        .m_methods = spam_methods,
    };

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


Definitions
===========

This table summarizes how various items are defined.

========================= ============= ==============
Item                      py2           py3
========================= ============= ==============
PyStr_*                   → PyString_*  → PyUnicode_*
PyBytes_*                 → PyString_*  ✔
PyUnicode_*               ✔             ✔
PyString_*                ✔             error
PyStr_AsUTF8AndSize       see below     ✔
PyInt_*                   ✔             → PyLong_*
PyLong_*                  ✔             ✔
PyModuleDef               see below     ✔
PyModuleDef_HEAD_INIT     → 0           ✔
PyModule_Create           see below     ✔
MODULE_INIT_FUNC          see below     see below
Rich comparison           ✔             ✔
PY_RICHCMP                see below     see below
Py_TYPE                   ✔             ✔
PyVarObject_HEAD_INIT     ✔             ✔
Py_TPFLAGS_HAVE_WEAKREFS  ✔             → 0
Py_TPFLAGS_HAVE_ITER      ✔             → 0
========================= ============= ==============

Legend:

    | ✔ – provided by Python
    | → – defined in py3c as a simple alias for

This library defines the following non-trivial macros:

    PyStr_AsUTF8AndSize
        Python 2: defined in terms of PyString_Size and PyString_AsString. Differences from Python 3:
          * size pointer must not be NULL
          * size may be stored even if an error occurs

    PyModuleDef
        | Python 2: contains ``m_name``, ``m_doc``, ``m_size``, ``m_methods`` fields from Python 3, and ``m_base`` to accomodate PyModuleDef_HEAD_INIT.

    PyModule_Create
        | Python 2: calls Py_InitModule3; semantics same as in Python 3

    MODULE_INIT_FUNC(<mod>)
        | Python 3: declares PyInit_<mod> and provides function header for it
        | Python 2: declares & defines PyInit_mod; declares init<mod> and provides function header for it

    PY3C_RICHCMP
        | See docs. (Purely a convenience macro, same in both versions.)
