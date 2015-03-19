===================
Definitions in py3c
===================

This table summarizes the various macros py3c defines.

============================ ============= ==============
Macro                        py2           py3
============================ ============= ==============
PyStr_*                      → PyString_*  → PyUnicode_*
PyBytes_*                    → PyString_*  ✔
PyUnicode_*                  ✔             ✔
PyString_*                   ✔             *error*
PyStr_AsUTF8AndSize          see below     ✔
PyInt_*                      ✔             → PyLong_*
PyLong_*                     ✔             ✔
PyModuleDef                  see below     ✔
PyModuleDef_HEAD_INIT        → 0           ✔
PyModule_Create              see below     ✔
MODULE_INIT_FUNC             see below     see below
Rich comparison              ✔             ✔
PY3C_RICHCMP                 see below     see below
Py_RETURN_NOTIMPLEMENTED     =             =
Py_TYPE                      ✔             ✔
Py_REFCNT                    ✔             ✔
Py_SIZE                      ✔             ✔
PyVarObject_HEAD_INIT        ✔             ✔
Py_TPFLAGS_HAVE_WEAKREFS     ✔             → 0
Py_TPFLAGS_HAVE_ITER         ✔             → 0
============================ ============= ==============

Legend:

    | ✔ – provided by Python
    | → – defined in py3c as a simple alias for
    | = – defined as in Python 3.4, for Pythons versions that don't define it

The following non-trivial macros are defined:

    PyStr_AsUTF8AndSize
        Python 2: defined in terms of PyString_Size and PyString_AsString. Differences from Python 3:
          * no encoding (string is assumed to be UTF-8-encoded)
          * size pointer must not be NULL
          * size may be stored even if an error occurs

    PyModuleDef
        | Python 2: contains ``m_name``, ``m_doc``, ``m_size``, ``m_methods`` fields from Python 3, and ``m_base`` to accomodate PyModuleDef_HEAD_INIT.

    PyModule_Create
        | Python 2: calls Py_InitModule3; semantics same as in Python 3

    MODULE_INIT_FUNC(<mod>)
        | Python 3: declares PyInit_<mod> and provides function header for it
        | Python 2: declares & defines PyInit_<mod>; declares init<mod> and provides function header for it

    PY3C_RICHCMP
        | See docs. (Purely a convenience macro, same in both versions.)
