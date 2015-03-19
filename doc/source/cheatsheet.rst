~~~~~~~~~~~~~~~~~~~
The py3c Cheatsheet
~~~~~~~~~~~~~~~~~~~

Strings
~~~~~~~

* PyStr_* – for human-readable strings

* PyBytes_* – for binary data

* PyUnicode_* – when you used ``unicode`` in Python 2

* PyString_* – when you don't care about Python 3 yet

Ints
~~~~

Use whatever you used in Python 2. For py3-only code, use ``PyLong``.

Comparison
~~~~~~~~~~

Use `rich comparisons <https://www.python.org/dev/peps/pep-0207/>`_.
A convenience macro, ``PY3C_RICHCMP(a, b, op)``, is provided to help common cases.

Objects & Types
~~~~~~~~~~~~~~~

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


CObject
~~~~~~~

Use the `PyCapsule <https://docs.python.org/3/c-api/capsule.html#capsules>`_ API.
If you need to support 2.6, you'll currently need ``#if PY_3`` blocks.
